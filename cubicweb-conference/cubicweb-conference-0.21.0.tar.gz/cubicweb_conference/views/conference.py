from datetime import date

from logilab.mtconverter import xml_escape
from logilab.common.date import date_range, ONEDAY

from cubicweb import _
from cubicweb.predicates import is_instance, rql_condition, match_user_groups
from cubicweb_web.view import EntityView
from cubicweb_web.views import tabs


class ConferencePrimaryView(tabs.TabbedPrimaryView):
    __select__ = is_instance("Conference")
    tabs = [
        _("confinfo"),
        _("talkslist"),
        _("talksschedule"),
        _("userconfschedule"),
        _("adminview"),
    ]
    default_tab = "confinfo"

    def render_entity_title(self, entity):
        self.w("<h1>%s</h1>" % xml_escape(entity.dc_long_title()))


class ConferenceInfoView(EntityView):
    __select__ = is_instance("Conference")
    __regid__ = "confinfo"

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        _ = self._cw._
        if entity.description:
            self.w("<div>%s</div>" % entity.dc_description("text/html"))
        rql = (
            "Any TR, TD, MIN(ST), MAX(ET), COUNT(T) GROUPBY TR, "
            "TD WHERE T? in_track TR, T start_time ST, T end_time ET, "
            "TR description TD, TR in_conf C, C eid %(c)s"
        )
        rset = self._cw.execute(rql, {"c": entity.eid})
        if rset:
            if entity.end_on > date.today():
                text = _("The conference will be divided into the following tracks:")
            else:
                text = _("The conference was divided into the following tracks:")
            self.w("<div>%s</div>" % text)
            headers = (
                _("Track title"),
                _("Description"),
                _("First talk"),
                _("Last talk"),
                _("Total talks"),
            )
            self.wview("table", rset, headers=headers, displaycols=range(0, 5))
        else:
            self.w("<div>%s</div>" % _("No track yet in this conference."))


class UserConfSchedule(EntityView):
    __select__ = is_instance("Conference") & ~match_user_groups("guests")
    __regid__ = "userconfschedule"

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        _ = self._cw._
        rql = (
            "Any T, ST, L ORDERBY ST WHERE T is Talk, T start_time ST, "
            "T location L, T in_conf C, C eid %(eid)s, U attend T, "
            "U login %(login)s"
        )
        rset = self._cw.execute(rql, {"eid": entity.eid, "login": self._cw.user.login})
        if rset:
            self.w("<p>%s</p>" % _("You are planning to attend these talks:"))
            self.wview(
                "table", rset, headers=(_("Talk title"), _("Date"), _("Location"))
            )
        else:
            self.w(
                "<p>%s</p>"
                % _(
                    "Do you plan to attend a specific talk ? Please click on "
                    "the attendancy button positionned at the top "
                    "right of each talk summary."
                )
            )


class ConferenceTalksList(EntityView):
    __select__ = is_instance("Conference")
    __regid__ = "talkslist"

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        _ = self._cw._
        rql = (
            "Any T, group_concat(U), ST, L, TR GROUPBY T, ST, L, TR "
            "ORDERBY ST WHERE T location L, T start_time ST, "
            "U leads T, T in_conf C, T in_track TR, T in_state S, T title TT, "
            'S name "accepted", C eid %(c)s'
        )
        rset = self._cw.execute(rql, {"c": entity.eid})
        if rset:
            headers = (
                _("Talk title"),
                _("Speaker"),
                _("Date"),
                _("Location"),
                _("Track"),
            )
            self.wview("table", rset, headers=headers, cellvids={1: "users_list"})
        else:
            self.w("<div>%s</div>" % _("No accepted talk yet in this conference"))


class ConferenceTalksSchedule(EntityView):
    __select__ = is_instance("Conference") & rql_condition("T in_conf X")
    __regid__ = "talksschedule"

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        tracks_rql = "Any TR WHERE TR in_conf C, TR is Track, C eid %(c)s"
        tracks = list(self._cw.execute(tracks_rql, {"c": entity.eid}).entities())
        for day in date_range(entity.start_on, entity.end_on + ONEDAY):
            self.w('<table style="width:100%">')
            self.w("<tr>")
            for track in tracks:
                if entity.has_talk(day, track):
                    rset = self._cw.execute(
                        "Any T WHERE T in_track TR, TR eid %(e)s, "
                        'T in_state S, S name "accepted"',
                        {"e": track.eid},
                    )
                    if rset:
                        self.w("<td>")
                        self.wview(
                            "onedaycal",
                            rset,
                            initargs={"day": day, "title": track.title},
                        )
                        self.w("</td>")
            self.w("</tr></table>")


class ConferenceAdminView(EntityView):
    __select__ = is_instance("Conference") & (
        match_user_groups("managers") | rql_condition("U is_chair_at X")
    )
    __regid__ = "adminview"

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(0, 0)
        # number of talks in each state
        self.w("<h2>%s</h2>" % self._cw._("Talk state details"))
        entity = self.cw_rset.get_entity(0, 0)
        rql = "Any S, COUNT(T) GROUPBY S WHERE T is Talk, T in_state S, T in_conf C, C eid %(eid)s"
        rset = self._cw.execute(rql, {"eid": entity.eid})
        self.wview("table", rset, "null")
        rset = self._cw.execute(
            'Any T WHERE T is Talk, T in_state S, S name "submitted"'
        )
        if rset:
            treid = self._cw.execute(
                'Any T WHERE T is Transition, T name "send to reviewer"'
            )[0][0]
            self.w('<div id="statreview">')
            self.w("<p>%s</p>" % self._cw._("Please, assign a reviewer to :"))
            self.w("<ul>")
            for talk in rset.entities():
                self.w(
                    '<li><a href="%s">%s</a></li>'
                    % (
                        xml_escape(talk.absolute_url(vid="statuschange", treid=treid)),
                        xml_escape(talk.title),
                    )
                )
            self.w("</ul></div>")
        # number of participant by talk
        self.w("<h2>%s</h2>" % self._cw._("Number of participant by Talk"))
        rql = "Any T, COUNT(A) GROUPBY T WHERE T is Talk, A attend T, T in_conf C, C eid %(eid)s"
        rset = self._cw.execute(rql, {"eid": entity.eid})
        self.wview("table", rset, "null")
