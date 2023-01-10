# -*- coding: utf-8 -*-
# :Project:   SoL -- Batch I/O
# :Created:   lun 09 feb 2009 10:29:38 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2013, 2014, 2015, 2016, 2018, 2019, 2020, 2020, 2021 Lele Gaifax
#

"""
This module implements some utilities, mainly related to importing and
exporting tourneys data in a portable format.

Scarry used an ``INI`` file and we had several drawbacks with it, mainly
because sending them with e-mail would result in data corruption.

SoL uses YAML_ or JSON_ instead, by default compressing the outcome with gzip.

.. _YAML: http://yaml.org/
.. _JSON: http://json.org/
"""

from datetime import datetime
from filecmp import cmp
from glob import glob
from gzip import GzipFile
from io import BytesIO, StringIO
from itertools import groupby
from operator import attrgetter
from os import unlink, utime
from os.path import exists, isdir, join, split
from tempfile import mktemp
from urllib.parse import urljoin
from urllib.request import urlopen
import logging
import sqlite3
import zipfile

from rapidjson import Decoder, Encoder, DM_ISO8601, NM_NATIVE, NM_DECIMAL
from ruamel.yaml import YAML

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from transaction import doom
from xlsxwriter import Workbook

from ..i18n import gettext, translatable_string as _
from . import (
    Board,
    Championship,
    Club,
    Competitor,
    Match,
    Player,
    Rate,
    Rating,
    Tourney,
    User,
    )
from .errors import OperationAborted, TourneyAlreadyExistsError, UnauthorizedOperation
from .utils import (
    asunicode,
    entity_from_primary_key,
    normalize,
    changes_summary,
    )


logger = logging.getLogger(__name__)
changes_logger = logging.getLogger(__name__ + '.changes')


# Here we use JSON codecs different from those used by Pyramid JSON renderer, because we do not
# want to coerce naïve timestamps to UTC as done there for human consumption in the UI

json_decode = Decoder(datetime_mode=DM_ISO8601,
                      number_mode=NM_NATIVE).__call__

json_encode = Encoder(datetime_mode=DM_ISO8601,
                      number_mode=NM_NATIVE | NM_DECIMAL,
                      ensure_ascii=False).__call__


class Serializer:
    """Serialize some SoL entities as flat dictionaries."""

    def __init__(self):
        self.id_map = {}
        "An hash mapping a particular instance to its serial marker"

        self.users = []
        "A list of serialized users"

        self.players = []
        "A list of serialized players"

        self.clubs = []
        "A list of serialized clubs"

        self.championships = []
        "A list of serialized championships"

        self.ratings = []
        "A list of serialized ratings"

        self.rates = []
        "A list of serialized rates"

        self.tourneys = []
        "A list of serialized tourneys"

        self.modified = datetime.min
        "Most recent modification timestamp of any serialized entity"

    def addClub(self, club):
        """Serialize a club, if not already done.

        :param club: a :py:class:`.Club` instance
        :rtype: int
        :returns: an integer marker that identify the given club
        """

        try:
            return self.id_map[(type(club), club.idclub)]
        except KeyError:
            self.clubs.append(None)
            idx = len(self.clubs)
            self.id_map[(type(club), club.idclub)] = idx
            self.clubs[idx-1] = club.serialize(self)
            if club.modified > self.modified:  # pragma: nocover
                self.modified = club.modified
            return idx

    def addChampionship(self, championship):
        """Serialize a championship, if not already done.

        :param club: a :py:class:`.Championship` instance
        :rtype: int
        :returns: an integer marker that identify the given championship
        """

        try:
            return self.id_map[(type(championship), championship.idchampionship)]
        except KeyError:
            self.championships.append(None)
            idx = len(self.championships)
            self.id_map[(type(championship), championship.idchampionship)] = idx
            self.championships[idx-1] = championship.serialize(self)
            if championship.modified > self.modified:  # pragma: nocover
                self.modified = championship.modified
            return idx

    def addRating(self, rating):
        """Serialize a rating, if not already done.

        :param rating: a :py:class:`.Rating` instance
        :rtype: int
        :returns: an integer marker that identify the given rating
        """

        try:
            return self.id_map[(type(rating), rating.idrating)]
        except KeyError:
            self.ratings.append(None)
            idx = len(self.ratings)
            self.id_map[(type(rating), rating.idrating)] = idx
            self.ratings[idx-1] = rating.serialize(self)
            if rating.modified > self.modified:  # pragma: nocover
                self.modified = rating.modified
            return idx

    def addPlayer(self, player):
        """Serialize a player, if not already done.

        :param player: a :py:class:`.Player` instance
        :rtype: int
        :returns: an integer marker that identify the given player
        """

        try:
            return self.id_map[(type(player), player.idplayer)]
        except KeyError:
            self.players.append(None)
            idx = len(self.players)
            self.id_map[(type(player), player.idplayer)] = idx
            self.players[idx-1] = player.serialize(self)
            if player.modified > self.modified:  # pragma: nocover
                self.modified = player.modified
            return idx

    def addRate(self, rate):
        """Serialize a rate, if not already done.

        :param rate: a :py:class:`.Rate` instance
        :rtype: int
        :returns: an integer marker that identify the given rate
        """

        try:
            return self.id_map[(type(rate), rate.idrate)]
        except KeyError:
            self.rates.append(None)
            idx = len(self.rates)
            self.id_map[(type(rate), rate.idrate)] = idx
            self.rates[idx-1] = rate.serialize(self)
            return idx

    def addTourney(self, tourney):
        """Serialize a tourney, if not already done.

        :param tourney: a :py:class:`.Tourney` instance
        :rtype: int
        :returns: an integer marker that identify the given tourney
        """

        try:
            return self.id_map[(type(tourney), tourney.idtourney)]
        except KeyError:
            self.tourneys.append(None)
            idx = len(self.tourneys)
            self.id_map[(type(tourney), tourney.idtourney)] = idx
            self.tourneys[idx-1] = tourney.serialize(self)
            if tourney.modified > self.modified:  # pragma: nocover
                self.modified = tourney.modified
            return idx

    def addUser(self, user):
        """Serialize a user, if not already done.

        :param user: a :py:class:`.User` instance
        :rtype: int
        :returns: an integer marker that identify the given user
        """

        try:
            return self.id_map[(type(user), user.iduser)]
        except KeyError:
            self.users.append(None)
            idx = len(self.users)
            self.id_map[(type(user), user.iduser)] = idx
            self.users[idx-1] = user.serialize(self)
            return idx

    def dump(self):
        yield dict(users=self.users,
                   players=self.players,
                   clubs=self.clubs,
                   championships=self.championships,
                   ratings=self.ratings,
                   rates=self.rates)
        for tourney in self.tourneys:
            yield tourney


class Deserializer:
    """Deserialize a flat representation of some SoL entities."""

    def __init__(self, session, idowner, update_only_missing_fields):
        self.update_only_missing_fields = update_only_missing_fields
        "A boolean flag, whether only missing fields will be updated."

        self.session = session
        "The SQLAlchemy session."

        self.idowner = idowner
        "The ID of the :py:class:`owner <.User>` of newly created instances."

        self.users = []
        "A list of :py:class:`users <.User>` instances."

        self.players = []
        "A list of :py:class:`players <.Player>` instances."

        self.clubs = []
        "A list of :py:class:`clubs <.Club>` instances."

        self.championships = []
        "A list of :py:class:`championships <.Championship>` instances."

        self.ratings = []
        "A list of :py:class:`ratings <.Rating>` instances."

        self.rates = []
        "A list of :py:class:`rates <.Rate>` instances."

        self.tourneys = []
        "A list of :py:class:`tourneys <.Tourney>` instances."

        self.skipped = 0
        "The number of skipped tournaments, because already present."

    def addClub(self, sclub):
        """Deserialize a :py:class:`.Club`.

        :param sclub: a dictionary containing the flatified representation
        :rtype: :py:class:`.Club`
        :returns: either an existing or a new instance
        """

        query = self.session.query

        guid = sclub.pop('guid', None)
        description = normalize(asunicode(sclub.pop('description')))

        club = None
        if guid is not None:
            club = query(Club).filter_by(guid=guid).one_or_none()

        if club is None:
            club = query(Club).filter_by(description=description).one_or_none()

        if 'owner' in sclub:
            sclub['owner'] = self.users[sclub['owner'] - 1]

        if 'users' in sclub:
            users = [self.users[u - 1] for u in sclub.pop('users')]
        else:
            users = None

        if club is None:
            if 'owner' not in sclub:
                sclub['idowner'] = self.idowner
            if users:
                sclub['users'] = users

            club = Club(guid=guid, description=description, **sclub)
            self.session.add(club)
            logger.info('New %r', club)
        else:
            smodified = sclub.get('modified')
            tmodified = club.modified

            if smodified is None or tmodified is None or smodified > tmodified:
                changes = club.update(sclub, missing_only=self.update_only_missing_fields)
                if changes:
                    logger.info('Updated %r: %s', club, changes_summary(changes))

            if users:
                suids = set(u.iduser for u in users)
                tuids = set(u.iduser for u in club.users)
                if tuids - suids:
                    for user in users:
                        if user.iduser not in tuids:
                            club.users.append(user)
                            logger.info('Updated %r: added user %r', club, user)

        self.clubs.append(club)

        return club

    def addPlayer(self, splayer):
        """Deserialize a :py:class:`.Player`.

        :param splayer: a dictionary containing the flatified representation
        :rtype: :py:class:`.Player`
        :returns: either an existing or a new instance
        """

        guid = splayer.pop('guid', None)
        lastname = normalize(asunicode(splayer.pop('lastname')), True)
        firstname = normalize(asunicode(splayer.pop('firstname')), True)
        nickname = asunicode(splayer.pop('nickname', None))

        # None may cause problems on some dbs...
        if nickname is None:
            nickname = ''

        # If the agreedprivacy is missing, assume we are loading a SoL3 dump
        if guid is None and splayer.get('agreedprivacy', 'A') != 'A':
            logger.warning('Inserting a crypted player, who did not agree with the privacy'
                           ' policy: %r (firstname=%s lastname=%s nickname=%s)',
                           splayer, firstname, lastname, nickname)

        # Forget about player's phone, may be present on SoL3 streams
        if 'phone' in splayer:
            splayer.pop('phone')

        try:
            player, merged_into = Player.find(self.session, lastname, firstname,
                                              nickname, guid)
        except MultipleResultsFound:
            raise OperationAborted(
                _('Refusing to guess the right player: more than one person with first'
                  ' name "$fname" and last name "$lname", and no nickname was specified',
                  mapping=dict(fname=firstname, lname=lastname)))

        merged = splayer.pop('merged', [])
        if 'owner' in splayer:
            splayer['owner'] = self.users[splayer['owner'] - 1]
        if 'club' in splayer:
            splayer['club'] = self.clubs[splayer['club'] - 1]
        if 'federation' in splayer:
            splayer['federation'] = self.clubs[splayer['federation'] - 1]

        if player is None:
            if splayer.get('agreedprivacy', 'A') != 'A':
                logger.warning('Inserting a crypted player, who did not agree with the privacy'
                               ' policy: %r (firstname=%s lastname=%s nickname=%s)',
                               splayer, firstname, lastname, nickname)

            if 'owner' not in splayer:
                splayer['idowner'] = self.idowner

            player = Player(guid=guid,
                            firstname=firstname, lastname=lastname, nickname=nickname,
                            **splayer)
            self.session.add(player)
            logger.info('New %r', player)
        else:
            smodified = splayer.get('modified')
            tmodified = player.modified

            # Do not update the player if the incoming data is related to
            # a person who has been merged into another player
            if not merged_into:
                if smodified is None or tmodified is None or smodified > tmodified:
                    changes = player.update(splayer,
                                            missing_only=self.update_only_missing_fields)
                    if changes:
                        logger.info('Updated %r: %s', player, changes_summary(changes))

        if merged:
            try:
                player.mergePlayers(merged)
            except OperationAborted as e:  # pragma: nocover
                logger.warning('Could not merge %r with %r: %s', player, merged, e)

        self.players.append(player)

        return player

    def addChampionship(self, schampionship):
        """Deserialize a :py:class:`.Championship`.

        :param schampionship: a dictionary containing the flatified representation
        :rtype: :py:class:`.Championship`
        :returns: either an existing or a new instance
        """

        query = self.session.query

        guid = schampionship.pop('guid', None)
        description = normalize(asunicode(schampionship.pop('description')))

        ssc = schampionship.pop('club')
        if isinstance(ssc, dict):
            # Old SoL 2
            club = self.addClub(ssc)
        else:
            club = self.clubs[ssc - 1]

        championship = None
        if guid is not None:
            championship = query(Championship).filter_by(guid=guid).one_or_none()

        if championship is None:
            championship = query(Championship).filter_by(description=description,
                                                         idclub=club.idclub).one_or_none()

        if 'rating' in schampionship:
            schampionship['rating'] = self.ratings[schampionship['rating'] - 1]

        if 'owner' in schampionship:
            schampionship['owner'] = self.users[schampionship['owner'] - 1]

        if 'prizefactor' in schampionship:
            # Old SoL 2 dump
            del schampionship['prizefactor']

        if championship is None:
            if 'owner' not in schampionship:
                schampionship['idowner'] = self.idowner

            championship = Championship(guid=guid, club=club, description=description,
                                        **schampionship)
            self.session.add(championship)
            logger.info('New %r', championship)
        else:
            smodified = schampionship.get('modified')
            tmodified = championship.modified

            if smodified is None or tmodified is None or smodified > tmodified:
                changes = championship.update(schampionship,
                                              missing_only=self.update_only_missing_fields)
                if changes:  # pragma: nocover
                    logger.info('Updated %r: %s', championship, changes_summary(changes))

        self.championships.append(championship)

        return championship

    def addRating(self, srating):
        """Deserialize a :py:class:`.Rating`.

        :param srating: a dictionary containing the flatified representation
        :rtype: :py:class:`.Rating`
        :returns: either an existing or a new instance
        """

        query = self.session.query

        guid = srating.pop('guid', None)
        description = normalize(asunicode(srating.pop('description')))

        rating = None
        if guid is not None:
            rating = query(Rating).filter_by(guid=guid).one_or_none()

        if rating is None:
            rating = query(Rating).filter_by(description=description).one_or_none()

        if 'owner' in srating:
            srating['owner'] = self.users[srating['owner'] - 1]

        if 'club' in srating:
            srating['club'] = self.clubs[srating['club'] - 1]

        if rating is None:
            if 'owner' not in srating:
                srating['idowner'] = self.idowner

            rating = Rating(guid=guid, description=description, **srating)
            self.session.add(rating)
            logger.info('New %r', rating)
        else:
            smodified = srating.get('modified')
            tmodified = rating.modified

            if smodified is None or tmodified is None or smodified > tmodified:
                changes = rating.update(srating, missing_only=self.update_only_missing_fields)
                if changes:  # pragma: nocover
                    logger.info('Updated %r: %s', rating, changes_summary(changes))

        self.ratings.append(rating)

        return rating

    def addRate(self, srate):
        """Deserialize a :py:class:`.Rate`.

        :param srate: a dictionary containing the flatified representation
        :rtype: :py:class:`.Rate`
        :returns: either an existing or a new instance
        """

        query = self.session.query

        rating = self.ratings[srate.pop('rating') - 1]
        player = self.players[srate.pop('player') - 1]
        date = srate.pop('date')

        rate = None
        try:
            rate = query(Rate).filter_by(idrating=rating.idrating,
                                         idplayer=player.idplayer,
                                         date=date).one()
        except NoResultFound:
            rate = Rate(rating=rating, player=player, date=date, **srate)
            self.session.add(rate)
        else:
            rate.update(srate)

        self.rates.append(rate)

        return rate

    def addTourney(self, stourney):
        """Deserialize a :py:class:`.Tourney`.

        :param stourney: a dictionary containing the flatified representation
        :rtype: :py:class:`.Tourney`
        :returns: either an existing or a new instance
        """

        query = self.session.query

        guid = stourney.pop('guid', None)
        date = stourney.pop('date')

        if 'season' in stourney:
            # SoL 3 renamed “season” to “championship”
            stc = stourney.pop('season')
            # but in SoL 2 there was also a “championship”, now gone
            stourney.pop('championship', None)
        else:
            stc = stourney.pop('championship')
        if isinstance(stc, dict):
            # Old SoL 2 dump
            championship = self.addChampionship(stc)
        else:
            championship = self.championships[stc - 1]
        if 'hosting_club' in stourney:
            stourney['hosting_club'] = self.clubs[stourney['hosting_club'] - 1]
        if 'owner' in stourney:
            stourney['owner'] = self.users[stourney['owner'] - 1]
        if 'description' in stourney:
            stourney['description'] = normalize(asunicode(stourney['description']))
        if 'location' in stourney:
            stourney['location'] = normalize(asunicode(stourney['location']))
        if 'prizes' in stourney:
            # Old SoL 2 allowed the tourney prize-giving-method to be
            # different from the campionship setting, non sense!
            del stourney['prizes']
        if 'rating' in stourney:
            stourney['rating'] = self.ratings[stourney['rating'] - 1]
        if 'prizefactor' in stourney:
            del stourney['prizefactor']
        competitors = stourney.pop('competitors')
        matches = stourney.pop('matches')

        tourney = None
        if guid is not None:
            tourney = query(Tourney).filter_by(guid=guid).one_or_none()

        if tourney is None:
            tourney = query(Tourney).filter_by(idchampionship=championship.idchampionship,
                                               date=date).one_or_none()

        if tourney is None:
            if 'owner' not in stourney:
                stourney['idowner'] = self.idowner

            ctors = stourney['competitors'] = []
            for c in competitors:
                ctor = Competitor()
                for i, p in enumerate(c.pop('players'), 1):
                    if isinstance(p, dict):
                        # Old SoL 2
                        c['player%d' % i] = self.addPlayer(p)
                    else:
                        c['player%d' % i] = self.players[p-1]
                ctor.update(c)
                ctors.append(ctor)

            mtchs = stourney['matches'] = []
            for m in matches:
                m['competitor1'] = (ctors[m['competitor1']-1]
                                    if m['competitor1'] else None)
                m['competitor2'] = (ctors[m['competitor2']-1]
                                    if m['competitor2'] else None)

                if 'misses1_1' in m:
                    # FIXME: v4beta, remove after 4.0final
                    boards = []
                    i = 1
                    while f'misses1_{i}' in m or f'misses2_{i}' in m:
                        boards.append({'number': i,
                                       'coins1': m.pop(f'misses1_{i}', None),
                                       'coins2': m.pop(f'misses2_{i}', None)})
                        i += 1
                else:
                    boards = m.pop('boards', ())
                m['boards'] = [Board(**b) for b in boards]

                match = Match(**m)
                mtchs.append(match)

            tourney = Tourney(guid=guid, championship=championship, date=date,
                              **stourney)
            self.session.add(tourney)
            logger.info('New %r', tourney)
        else:
            # Don't allow updates to existing completed tourneys
            if tourney.matches or tourney.prized or any(
                    c for c in tourney.competitors if c.points or c.bucholz):
                raise TourneyAlreadyExistsError(
                    _('Tourney "$tourney" of championship "$championship" by "$club" on'
                      ' $date already present, cannot update it', mapping=dict(
                          tourney=tourney.description,
                          date=date.strftime(str(gettext('%m-%d-%Y'))),
                          club=championship.club.description,
                          championship=championship.description)),
                    tourney)
            else:
                # We are reloading a not-yet-played tourney, so we are going
                # to renew its list of competitors: delete existing ones
                while tourney.competitors:
                    c = tourney.competitors.pop()
                    self.session.delete(c)
                self.session.flush()

                smodified = stourney.get('modified')
                tmodified = tourney.modified

                if smodified is None or tmodified is None or smodified > tmodified:
                    ctors = tourney.competitors
                    players = self.players
                    for c in competitors:
                        ctor = Competitor()
                        for i, p in enumerate(c.pop('players'), 1):
                            if isinstance(p, dict):  # pragma: nocover
                                # Old SoL 2
                                c['player%d' % i] = self.addPlayer(p)
                            else:
                                c['player%d' % i] = players[p-1]
                        ctor.update(c)
                        ctors.append(ctor)

                    for m in matches:
                        m['competitor1'] = (ctors[m['competitor1']-1]
                                            if m['competitor1'] else None)
                        m['competitor2'] = (ctors[m['competitor2']-1]
                                            if m['competitor2'] else None)
                        match = Match(**m)
                        tourney.matches.append(match)

                    changes = tourney.update(stourney,
                                             missing_only=self.update_only_missing_fields)
                    if changes:  # pragma: nocover
                        logger.info('Updated %r: %s', tourney, changes_summary(changes))

        self.tourneys.append(tourney)

        return tourney

    def addUser(self, suser):
        """Deserialize a :py:class:`.User`.

        :param suser: a dictionary containing the flatified representation
        :rtype: :py:class:`.User`
        :returns: either an existing or a new instance
        """

        query = self.session.query

        email = asunicode(suser.pop('email', None))

        if email is not None:
            email = email.strip()

        # Do not allow changing password by upload
        suser.pop('password', None)
        suser.pop('_password', None)

        if not email:
            raise OperationAborted(_('Could not add user, its email is missing!'))

        try:
            user = query(User).filter_by(email=email).one()
        except NoResultFound:
            user = User(email=email, **suser)
            self.session.add(user)
        else:
            user.update(suser)

        self.users.append(user)

        return user

    def load(self, dump):
        users_by_email = None

        for data in dump:
            if 'clubs' in data:
                users = data.get('users')
                if users is None:
                    users_by_email = {}
                    # SoL3 archive: synthetize a separate users list
                    users = []
                    players = data.get('players')
                    for name in ('seasons', 'championships', 'clubs', 'players', 'ratings'):
                        for simple in data.get(name, ()):
                            if 'owner' not in simple:
                                continue
                            splayer = players[simple['owner'] - 1]
                            suser = {'lastname': splayer['lastname'],
                                     'firstname': splayer['firstname']}
                            email = splayer.get('email')
                            if not email:
                                email = '%(lastname)s.%(firstname)s@fake.com' % suser
                            if email in users_by_email:
                                simple['owner'] = users_by_email[email]
                            else:
                                suser['email'] = email
                                try:
                                    uidx = users.index(suser)
                                except ValueError:
                                    uidx = len(users)
                                    users.append(suser)
                                simple['owner'] = users_by_email[email] = uidx + 1

                for simple in users:
                    self.addUser(simple)

                pending_clubs_to_ratings = []

                for simple in data.get('clubs', ()):
                    rating = simple.pop('rating', None)
                    club = self.addClub(simple)
                    if rating is not None:
                        pending_clubs_to_ratings.append((club, rating))

                for simple in data.get('players', ()):
                    self.addPlayer(simple)

                for simple in data.get('ratings', ()):
                    self.addRating(simple)

                for club, rating in pending_clubs_to_ratings:
                    club.rating = self.ratings[rating - 1]

                for simple in data.get('rates', ()):
                    self.addRate(simple)

                if 'seasons' in data:
                    # Old name for championships
                    championships = data.get('seasons')
                else:
                    championships = data.get('championships', ())

                pending_chained_instances = []

                for simple in championships:
                    previous = simple.pop('previous', None)
                    cship = self.addChampionship(simple)
                    if previous is not None:
                        pending_chained_instances.append((cship, previous))

                for instance, previous in pending_chained_instances:
                    try:
                        previdx = previous - 1
                    except TypeError:
                        # Old SoL 2 dump
                        previdx = None
                        for i, s in enumerate(self.championships):
                            if s.description == previous and s.club is instance.club:
                                previdx = i
                                break

                        if previdx is None:
                            try:
                                pchampionship = self.session.query(Championship).filter_by(
                                    description=previous, idclub=instance.club.idclub).one()
                            except NoResultFound:
                                logger.warning('Could not find previous championship "%s"'
                                               ' for %r', previous, instance)
                            else:
                                instance.previous = pchampionship

                    if previdx is not None:
                        instance.previous = self.championships[previdx]
            else:
                if users_by_email is not None and 'owner' in data:
                    # SoL3 archive
                    player = self.players[data['owner'] - 1]
                    suser = {'lastname': player.lastname,
                             'firstname': player.firstname}
                    email = player.email
                    if not email:
                        email = '%(lastname)s.%(firstname)s@fake.com' % suser
                    if email in users_by_email:  # pragma: nocover
                        data['owner'] = users_by_email[email]
                    else:
                        for user_index, user in enumerate(self.users):
                            if user.email == email:  # pragma: nocover
                                break
                        else:
                            suser['email'] = email
                            user_index = len(self.users)
                            user = self.addUser(suser)
                        data['owner'] = users_by_email[email] = user_index + 1

                try:
                    self.addTourney(data)
                except TourneyAlreadyExistsError as e:  # pragma: no cover
                    logger.info('Tourney "%s" of championship "%s" by club "%s" on'
                                ' %s already present, cannot update it' % (
                                    e.tourney.description,
                                    e.tourney.championship.description,
                                    e.tourney.championship.club.description,
                                    e.tourney.date.strftime('%m-%d-%Y')))
                    self.skipped += 1


class TourneyXlsxDumper:
    """Create a XLSX document from a single tournament.

    :param tourney: a :py:class:`.Tourney` instance

    Create a simple Excel spreadsheet containing several sheets with its competitors,
    matches and ranking.
    """

    def __init__(self, tourney):
        self.tourney = tourney
        self.output = BytesIO()
        self.workbook = Workbook(self.output, {'in_memory': True})
        self.header_format = self.workbook.add_format({'bold': True, 'align': 'center'})

    def __call__(self):
        self.write_tourney()
        self.write_competitors()
        self.write_matches()
        self.write_ranking()
        self.workbook.close()
        return self.output.getvalue()

    def write_tourney(self):
        date_format = self.workbook.add_format({'num_format': 'd mmmm yyyy',
                                                'align': 'center'})
        right_format = self.workbook.add_format({'bold': True, 'align': 'right'})
        center_format = self.workbook.add_format({'align': 'center'})
        sheet = self.workbook.add_worksheet(gettext('Tourney'))
        sheet.set_column(0, 0, 15)
        sheet.set_column(1, 1, 40)
        sheet.write(0, 0, gettext('Tourney'), right_format)
        sheet.write(0, 1, self.tourney.description, center_format)
        sheet.write(1, 0, gettext('Location'), right_format)
        sheet.write(1, 1, self.tourney.location, center_format)
        sheet.write(2, 0, gettext('Date'), right_format)
        sheet.write(2, 1, self.tourney.date, date_format)
        sheet.write(3, 0, gettext('Club'), right_format)
        sheet.write(3, 1, self.tourney.championship.club.description, center_format)
        sheet.write(4, 0, gettext('Championship'), right_format)
        sheet.write(4, 1, self.tourney.championship.description, center_format)

    def write_competitors(self):
        sheet = self.workbook.add_worksheet(gettext('Competitors'))
        sheet.write(0, 0, gettext('#'), self.header_format)
        sheet.set_column(0, 0, 5)
        sheet.write(0, 1, gettext('Competitor'), self.header_format)
        sheet.set_column(1, 1, 30)

        for row, c in enumerate(self.tourney.competitors, 2):
            sheet.write(row, 0, row - 1)
            sheet.write(row, 1, c.caption(html=False))

    def write_matches(self):
        for turn, matches in groupby(self.tourney.matches, attrgetter('turn')):
            sheet = self.workbook.add_worksheet(gettext('Turn %d') % turn)
            sheet.write(0, 0, gettext('Board'), self.header_format)
            sheet.set_column(0, 0, 5)
            sheet.write(0, 1, gettext('Competitor 1'), self.header_format)
            sheet.set_column(1, 1, 30)
            sheet.write(0, 2, gettext('Competitor 2'), self.header_format)
            sheet.set_column(2, 2, 30)
            sheet.write(0, 3, gettext('Score 1'), self.header_format)
            sheet.set_column(3, 3, 8)
            sheet.write(0, 4, gettext('Score 2'), self.header_format)
            sheet.set_column(4, 4, 8)

            for row, m in enumerate(list(matches), 2):
                sheet.write(row, 0, row - 1)
                sheet.write(row, 1, m.competitor1.caption(html=False))
                if m.competitor2 is not None:
                    sheet.write(row, 2, m.competitor2.caption(html=False))
                else:
                    sheet.write(row, 2, gettext('Phantom'))
                sheet.write(row, 3, m.score1)
                sheet.write(row, 4, m.score2)

    def write_ranking(self):
        sheet = self.workbook.add_worksheet(gettext('Ranking'))
        sheet.write(0, 0, gettext('Rank'), self.header_format)
        sheet.set_column(0, 0, 5)
        sheet.write(0, 1, gettext('Competitor'), self.header_format)
        sheet.set_column(1, 1, 30)
        sheet.write(0, 2, gettext('Points'), self.header_format)
        sheet.set_column(2, 2, 8)
        sheet.write(0, 3, gettext('Bucholz'), self.header_format)
        sheet.set_column(3, 3, 8)
        sheet.write(0, 4, gettext('Score'), self.header_format)
        sheet.set_column(4, 4, 8)
        if self.tourney.prized:
            sheet.write(0, 5, gettext('Prize'), self.header_format)
            sheet.set_column(5, 5, 8)

        for row, c in enumerate(self.tourney.ranking, 2):
            sheet.write(row, 0, row - 1)
            sheet.write(row, 1, c.caption(html=False))
            sheet.write(row, 2, c.points)
            sheet.write(row, 3, c.bucholz)
            sheet.write(row, 4, c.netscore)
            if self.tourney.prized:
                sheet.write(row, 5, c.prize)


def backup(sasess, pdir, edir, location=None, keep_only_if_changed=True,
           only_played_tourneys=False, serialization_format='yaml',
           native_when_possible=False, keep_max=30):
    """Dump almost everything in a ZIP file.

    :param sasess: a SQLAlchemy session
    :param pdir: the base path of the portrait images, ``sol.portraits_dir``
    :param edir: the base path of the emblem images, ``sol.emblems_dir``
    :param location: either None or a string
    :param keep_only_if_changed: a boolean flag
    :param only_played_tourneys: a boolean flag
    :param str serialization_format: either ``yaml`` or ``json``
    :param bool native_when_possible: if ``True``, use the native__ interface to perform the
                                      backup
    :param int keep_max: the number of previous backups that will be kept
    :rtype: bytes
    :return: the ZIP archive

    This function builds a ``ZIP`` archive containing a database dump and two subdirectories
    ``portraits`` and ``emblems``, respectively containing the images associated to the players
    and to the clubs. When `native_when_possible` is ``True`` and the underlying system permits
    it the dump is a complete backup of the database, otherwise it is a standard ``.sol`` dump
    made with :func:`dump_sol` named ``everything.sol`` with *all* tourneys and *all* players
    (that is, not just those who actually played).

    If `location` is given, it may be either the full path name of the output file where the
    backup will be written or the path of a directory. In the latter case the file name will be
    automatically computed using current time, giving something like
    ``sol-backup_2014-02-03T14:35:12.zip``.

    When `keep_only_if_changed is ``True`` (the default) and `location` is a directory, the
    newly generated backup will be compared with the previous one (if there is at least one, of
    course) and if nothing has changed it will be removed.

    When `only_played_tourneys` is ``True`` (the default is ``False``), the tourneys "in
    preparation" (that is, those without played matches) are ignored and not included in the
    dump.

    At the end, only the the most recent `keep_max` backups will be kept, deleting those in
    excess, starting from the oldest.

    __ https://docs.python.org/3.7/library/sqlite3.html#sqlite3.Connection.backup
    """

    logger.debug('Backing up whole database...')

    if location is None:
        backupfn = mktemp(prefix='sol')
    else:
        if isdir(location):
            now = datetime.now()
            backupfn = join(location,
                            now.strftime('sol-backup_%Y-%m-%dT%H:%M:%S.zip'))
        else:  # pragma: no cover
            keep_only_if_changed = False
            if exists(location):
                raise OperationAborted(
                    "The backup file “%s” does already exist!" % location)

    out = BytesIO()
    zipf = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)

    native_bck_fn = None
    if native_when_possible:
        sac = sasess.connection()
        if hasattr(sac.connection, 'backup'):
            native_bck_fn = mktemp(prefix='sol')

            if sasess.bind.url.database == ':memory:' and sac.connection.in_transaction:
                # Force a commit on the test database, otherwise the backup() stucks
                sac.connection.execute('commit')  # pragma: nocover

            with sqlite3.connect(native_bck_fn) as bck:
                sac.connection.backup(bck)

            zipf.write(native_bck_fn, 'everything.sqlite3')

    if native_bck_fn is None:
        serializer = Serializer()

        # Dump all players
        for player in sasess.query(Player) \
                            .options(joinedload('merged')) \
                            .order_by(Player.lastname, Player.firstname):
            serializer.addPlayer(player)

        # Dump all player's rates
        for rate in sasess.query(Rate) \
                          .options(joinedload('player')) \
                          .order_by(Rate.idrating, Rate.date):
            serializer.addRate(rate)

        # Dump all played tourneys, possibly ignoring those "in preparation", i.e. without
        # matches
        for tourney in sasess.query(Tourney).order_by(Tourney.date):
            if not only_played_tourneys or tourney.rankedturn > 0:
                serializer.addTourney(tourney)

        dump = serializer.dump()
        if serialization_format == 'yaml':
            stream = StringIO()
            yaml = YAML(typ='safe')
            yaml.dump_all(dump, stream)
            data = stream.getvalue()
        else:
            data = json_encode(list(dump))

        content = open(mktemp(prefix='sol'), 'w', encoding='utf-8')
        try:
            content.write(data)
            content.close()
            if serializer.modified != datetime.min:
                modified_ts = serializer.modified.timestamp()
                utime(content.name, (modified_ts, modified_ts))

            zipf.write(content.name, 'everything.sol')

            for player in serializer.players:
                if 'portrait' in player:
                    portrait = join(pdir, player['portrait'])
                    if exists(portrait):  # pragma: no cover
                        zipf.write(portrait, 'portraits/' + player['portrait'])

            for club in serializer.clubs:
                if 'emblem' in club:
                    emblem = join(edir, club['emblem'])
                    if exists(emblem):  # pragma: no cover
                        zipf.write(emblem, 'emblems/' + club['emblem'])

            zipf.close()
        finally:
            try:
                unlink(content.name)
            except OSError:  # pragma: no cover
                pass
    else:
        ptc = Player.__table__.c
        for portrait, in sasess.execute(select([ptc.portrait]).where(ptc.portrait != None)):
            imagefn = join(pdir, portrait)
            if exists(imagefn):  # pragma: no cover
                zipf.write(imagefn, 'portraits/' + portrait)

        ctc = Club.__table__.c
        for emblem, in sasess.execute(select([ctc.emblem]).where(ctc.emblem != None)):
            imagefn = join(pdir, emblem)
            if exists(imagefn):  # pragma: no cover
                zipf.write(imagefn, 'emblems/' + emblem)

        zipf.close()

    zip = out.getvalue()

    if location is not None:
        with open(backupfn, 'wb') as f:
            f.write(zip)

        removed = False
        if keep_only_if_changed:
            all_backups = glob(join(location, "sol-backup_*.zip"))
            if len(all_backups) > 1:  # pragma: no cover
                all_backups.sort()
                previous_backup = all_backups[-2]

                if cmp(previous_backup, backupfn, shallow=False):
                    unlink(backupfn)
                    removed = True
                    logger.debug('Nothing changed since %s', previous_backup)

        if not removed:
            logger.info('New backup written to %s', backupfn)

            all_backups = glob(join(location, "sol-backup_*.zip"))
            all_backups.sort()

            while len(all_backups) > keep_max:
                old_backup = all_backups.pop(0)
                unlink(old_backup)
                logger.info('Removed old backup %s', old_backup)

    return zip


def restore(sasess, pdir=None, edir=None, url=None, content=None, idowner=None):
    """Restore everything from a backup.

    :param sasess: a SQLAlchemy session
    :param pdir: the base path of the portrait images, ``sol.portraits_dir``
    :param edir: the base path of the emblem images, ``sol.emblems_dir``
    :param url: the URL of the file containing the archive, or None
    :param content: the content of the archive
    :param idowner: the ID of the responsible for newly created instances
    :rtype: tuple
    :return: the list of loaded tourney instances and the number of skipped tourneys

    This reads the ``ZIP`` created by :func:`backup` and loads its content into the database,
    writing the images in the right place (pre-existing images **won't** be overwritten,
    though).
    """

    if content is None:  # pragma: no cover
        assert url, "Must provide either a file or an URL!"
        url = urljoin('file:', url)
        logger.info('Retrieving %s', url)
        content = BytesIO(urlopen(url).read())

    zipf = zipfile.ZipFile(content, 'r')
    names = zipf.namelist()

    if 'everything.sol' not in names:  # pragma: nocover
        # TODO: decide whether restoring from everything.sqlite3 is possible/reasonable
        raise OperationAborted(
            "Invalid archive, does not contain the required “everything.sol”!")

    content = BytesIO(zipf.read('everything.sol'))
    tourneys, skipped = load_sol(sasess, 'everything.sol', content, True, idowner)

    names.sort()

    for name in names:
        if pdir is not None and name.startswith('portraits/'):
            portrait = join(pdir, split(name)[1])
            if not exists(portrait):
                outfile = open(portrait, 'wb')
                outfile.write(zipf.read(name))
                outfile.close()
            else:  # pragma: nocover
                logger.debug('Not overwriting %s', portrait)
        elif edir is not None and name.startswith('emblems/'):
            emblem = join(edir, split(name)[1])
            if not exists(emblem):
                outfile = open(emblem, 'wb')
                outfile.write(zipf.read(name))
                outfile.close()
            else:  # pragma: no cover
                logger.debug('Not overwriting %s', emblem)

    return tourneys, skipped


def load_sol(sasess, url=None, content=None, restore=False, idowner=None):
    """Load the archive exported from SoL.

    :param sasess: a SQLAlchemy session
    :param url: the URL of the ``.sol`` (or ``.sol.gz``) file
    :param content: the content of a ``.sol`` (or ``.sol.gz``) file
    :param restore: whether this is a restore, ``False`` by default
    :param idowner: the ID of the responsible for newly created instances
    :rtype: tuple
    :return: the list of loaded tourney instances and number of skipped tournaments

    If `content` is not specified, it will be loaded with ``urlopen()`` from the given `url`.

    Normally only missing data is updated, except when `restore` is True.
    """

    if content is None:
        assert url, "Must provide either a file or an URL!"
        url = urljoin('file:', url)
        logger.info('Retrieving %s', url)
        content = BytesIO(urlopen(url).read())

    if url and url.endswith('.sol.gz'):
        content = GzipFile(fileobj=content, mode='rb')

    data = content.read()

    deserializer = Deserializer(sasess, idowner, not restore)
    if data.startswith(b'[' if isinstance(data, bytes) else '['):
        data = json_decode(data)
    else:
        yaml = YAML(typ='safe')
        data = yaml.load_all(data)
    deserializer.load(data)

    for rating in deserializer.ratings:
        mindate = None
        for t in deserializer.tourneys:
            if t.rating is rating:
                if mindate is None or mindate > t.date:
                    mindate = t.date

        rating.recompute(mindate)

    return deserializer.tourneys, deserializer.skipped


def dump_sol(tourneys, gzipped=False, serialization_format='yaml'):
    """Dump tourneys as a YAML or JSON document.

    :param tourneys: the sequence of tourneys to dump
    :param gzipped: a boolean indicating whether the output will be compressed
                    with ``gzip``
    :param serialization_format: a string, either ``yaml`` or ``json``
    :rtype: bytes
    :return: the YAML/JSON document, possibly gzipped
    """

    serializer = Serializer()

    for tourney in tourneys:
        serializer.addTourney(tourney)

    dump = serializer.dump()
    if serialization_format == 'yaml':
        yaml = YAML(typ='safe')
        stream = StringIO()
        yaml.dump_all(dump, stream)
        data = stream.getvalue()
    else:
        data = json_encode(list(dump))

    if gzipped:
        out = BytesIO()
        gzipped = GzipFile(fileobj=out, mode='wb')
        gzipped.write(data.encode('utf-8'))
        gzipped.close()
        data = out.getvalue()

    return data


def _save_image(dir, fname, data, clogger):
    """Save an image and return its name.

    :param dir: the directory where to store the image
    :param fname: the uploaded file name
    :param data: a data-uri encoded image
    :param clogger: where to log applied changes
    :rtype: string
    :return: the filename where the image was written
    """

    from base64 import decodebytes
    from hashlib import md5
    from os.path import exists, join

    if not data.startswith('data:image'):  # pragma: nocover
        raise OperationAborted('Image is not a data URI')

    kind = data[data.index('/')+1:data.index(';')]
    data = decodebytes(data[data.index(',')+1:].encode('ascii'))

    newname = md5(data).hexdigest() + '.' + kind
    fullname = join(dir, newname)

    if not exists(fullname):
        with open(fullname, 'wb') as f:
            f.write(data)
        clogger.info('Wrote new image "%s" as "%s"', fname, fullname)
    else:  # pragma: nocover
        logger.debug('Image "%s" already exists as "%s"', fname, fullname)

    return newname


def _delete_image(dir, fname, clogger):
    """Delete an image.

    :param dir: the directory containing the image
    :param fname: the image file name
    :param clogger: where to log applied changes
    """

    fullname = join(dir, fname)
    if exists(fullname):
        unlink(fullname)
        logger.info('Deleted image "%s"', fullname)


def save_changes(sasess, request, modified, deleted, clogger=changes_logger):
    """Save insertions, changes and deletions to the database.

    :param sasess: the SQLAlchemy session
    :param request: the Pyramid web request
    :param modified: a sequence of record changes, each represented by
                     a tuple of two items, the PK name and a
                     dictionary with the modified fields; if the value
                     of the PK field is null or 0 then the record is
                     considered new and will be inserted instead of updated
    :param deleted: a sequence of deletions, each represented by a tuple
                    of two items, the PK name and the ID of the record to
                    be removed
    :param clogger: where to log applied changes
    :rtype: tuple
    :return: three lists, respectively inserted, modified and deleted record IDs,
             grouped in a dictionary keyed on PK name
    """

    iids = []
    mids = []
    dids = []

    if request is not None:
        settings = request.registry.settings
        pdir = settings['sol.portraits_dir']
        edir = settings['sol.emblems_dir']
        rsession = request.session
        user_id = rsession['user_id']
        is_admin = rsession['is_admin']
        is_ownersadmin = rsession['is_ownersadmin']
        is_playersmanager = rsession['is_playersmanager']
    else:
        # tests
        from tempfile import gettempdir
        edir = pdir = gettempdir()
        user_id = None
        is_admin = is_ownersadmin = is_playersmanager = False

    # Perform insertions after updates: this is to handle the corner
    # case on competitors in team events, when a player can be moved
    # from an existing team to a new one
    inserted = []
    pending_image = None

    for key, mdata in modified:
        entity = entity_from_primary_key(key)
        table = entity.__table__

        fvalues = {}
        for f, v in mdata.items():
            if (((f in table.c and f != key)
                 or (entity is Match and f.startswith(('coins1_', 'coins2_', 'queen_'))))):
                if v != '':
                    fvalues[f] = v
                else:
                    fvalues[f] = None
            elif f == 'image' and v:
                # Must be either a new emblem or a new portrait
                if entity is Player:
                    fname = mdata["portrait"]
                    pending_image = ('portrait', pdir, fname, v)
                elif entity is Club:
                    fname = mdata["emblem"]
                    pending_image = ('emblem', edir, fname, v)

        # If there are no changes, do not do anything
        if not fvalues:  # pragma: nocover
            continue

        # Set the modified timestamp, if the entity has it
        if hasattr(entity, 'modified'):
            fvalues['modified'] = func.now()

        # If the PK is missing or None, assume it's a new record
        idrecord = int(mdata.get(key) or 0)

        if idrecord == 0:
            if not is_playersmanager and entity is Player:
                # Abort current transaction
                doom()
                raise UnauthorizedOperation(_("Cannot manage players!"))

            if pending_image is not None:
                a, d, f, v = pending_image
                pending_image = None
                fvalues[a] = mdata[a] = _save_image(d, f, v, clogger)

            inserted.append((entity, key, fvalues))
        else:
            instance = sasess.query(entity).get(idrecord)
            if instance is not None:
                if not is_ownersadmin:
                    if hasattr(entity, 'idowner') and instance.idowner != user_id:
                        # Abort current transaction
                        doom()
                        logger.warning('Unauthorized attempt to modify %r', instance)
                        raise UnauthorizedOperation(_("Cannot modify not owned records!"))

                if not is_playersmanager and entity is Player:
                    # Abort current transaction
                    doom()
                    logger.warning('Unauthorized attempt to modify %r', instance)
                    raise UnauthorizedOperation(_("Cannot manage players!"))

                if pending_image is not None:
                    a, d, f, v = pending_image
                    pending_image = None
                    fvalues[a] = mdata[a] = _save_image(d, f, v, clogger)
                elif entity is Player and 'portrait' in mdata:
                    fname = mdata["portrait"]
                    if not fname and instance.portrait:
                        _delete_image(pdir, instance.portrait, clogger)
                elif entity is Club and 'emblem' in mdata:
                    fname = mdata["emblem"]
                    if not fname and instance.emblem:
                        _delete_image(edir, instance.emblem, clogger)

                mids.append({key: idrecord})
                changes = instance.update(fvalues)
                sasess.flush()
                csummary = changes_summary(changes)
                if csummary:
                    csummary = ': ' + csummary
                clogger.info('Updated %r%s', instance, csummary)

    for entity, key, fvalues in inserted:
        try:
            entity.check_insert(sasess, fvalues, 'admin' if is_admin else user_id)
        except Exception as e:
            clogger.error('Error trying to insert %r with %r: %s', entity, fvalues, e)
            raise

        if user_id is not None and hasattr(entity, 'idowner'):
            fvalues['idowner'] = user_id

        instance = entity(**fvalues)
        sasess.add(instance)
        sasess.flush()
        nextid = getattr(instance, key)
        iids.append({key: nextid})
        clogger.info('Inserted new %r', instance)

    for key, ddata in deleted:
        entity = entity_from_primary_key(key)
        instance = sasess.query(entity).get(ddata)
        if instance is not None:
            if user_id is not None:  # pragma: no cover
                if hasattr(entity, 'idowner') and instance.idowner != user_id:
                    # Abort current transaction
                    doom()
                    logger.warning('Unauthorized attempt to delete %r', instance)
                    raise UnauthorizedOperation(_("Cannot delete not owned records!"))

            instance.delete()
            dids.append({key: ddata})
            clogger.info('Deleted %r', instance)

    return iids, mids, dids
