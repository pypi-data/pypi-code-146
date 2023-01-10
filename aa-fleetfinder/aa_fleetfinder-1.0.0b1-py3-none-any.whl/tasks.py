"""
Tasks
"""

# Standard Library
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third Party
from bravado.exception import HTTPNotFound
from celery import shared_task

# Django
from django.core.cache import cache
from django.utils import timezone

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce
from esi.models import Token

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Fleet Finder
from fleetfinder import __title__
from fleetfinder.constants import (
    CACHE_KEY_FLEET_CHANGED_ERROR,
    CACHE_KEY_NO_FLEET_ERROR,
    CACHE_KEY_NO_FLEETBOSS_ERROR,
    CACHE_KEY_NOT_IN_FLEET_ERROR,
    CACHE_MAX_ERROR_COUNT,
    TASK_DEFAULT_KWARGS,
)
from fleetfinder.models import Fleet
from fleetfinder.providers import esi

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@shared_task
def open_fleet(character_id, motd, free_move, name, groups):
    """
    Open a fleet
    :param character_id:
    :param motd:
    :param free_move:
    :param name:
    :param groups:
    :return:
    """

    required_scopes = ["esi-fleets.read_fleet.v1", "esi-fleets.write_fleet.v1"]
    token = Token.get_token(character_id, required_scopes)

    fleet_result = esi.client.Fleets.get_characters_character_id_fleet(
        character_id=token.character_id, token=token.valid_access_token()
    ).result()
    fleet_id = fleet_result.pop("fleet_id")
    fleet_role = fleet_result.pop("role")

    if fleet_id is None or fleet_role is None or fleet_role != "fleet_commander":
        return

    fleet_commander = EveCharacter.objects.get(character_id=token.character_id)

    fleet = Fleet(
        fleet_id=fleet_id,
        created_at=timezone.now(),
        motd=motd,
        is_free_move=free_move,
        fleet_commander=fleet_commander,
        name=name,
    )
    fleet.save()
    fleet.groups.set(groups)

    esi_fleet = {"is_free_move": free_move, "motd": motd}
    esi.client.Fleets.put_fleets_fleet_id(
        fleet_id=fleet_id, token=token.valid_access_token(), new_settings=esi_fleet
    ).result()


@shared_task
def send_fleet_invitation(character_ids, fleet_id):
    """
    Send a fleet invitation through the eve client
    :param character_ids:
    :param fleet_id:
    """

    required_scopes = ["esi-fleets.write_fleet.v1"]
    fleet = Fleet.objects.get(fleet_id=fleet_id)
    fleet_commander_token = Token.get_token(
        fleet.fleet_commander.character_id, required_scopes
    )
    _processes = []

    with ThreadPoolExecutor(max_workers=50) as ex:
        for _character_id in character_ids:
            _processes.append(
                ex.submit(
                    send_invitation,
                    character_id=_character_id,
                    fleet_commander_token=fleet_commander_token,
                    fleet_id=fleet_id,
                )
            )

    for item in as_completed(_processes):
        _ = item.result()


@shared_task
def send_invitation(character_id, fleet_commander_token, fleet_id):
    """
    Open the fleet invite window in the eve client
    :param character_id:
    :param fleet_commander_token:
    :param fleet_id:
    """

    invitation = {"character_id": character_id, "role": "squad_member"}

    esi.client.Fleets.post_fleets_fleet_id_members(
        fleet_id=fleet_id,
        token=fleet_commander_token.valid_access_token(),
        invitation=invitation,
    ).result()


def close_esi_fleet(fleet: Fleet, reason: str) -> None:
    """
    Closing registered fleet
    :param fleet:
    :param reason:
    """

    fleet_id = fleet.fleet_id

    logger.info(f"Closing fleet with ID {fleet_id}. Reason: {reason}")

    fleet.delete()


def esi_fleetadvert_error_handling(
    cache_key: str, fleet: Fleet, logger_message: str
) -> None:
    """
    ESI error handling
    :param cache_key:
    :param fleet:
    :param logger_message:
    """

    if int(cache.get(cache_key + str(fleet.fleet_id))) < CACHE_MAX_ERROR_COUNT:
        error_count = int(cache.get(cache_key + str(fleet.fleet_id)))

        error_count += 1

        logger.info(f'"{logger_message}" Error Count: {error_count}.')

        cache.set(cache_key + str(fleet.fleet_id), str(error_count), 75)
    else:
        close_esi_fleet(fleet=fleet, reason=logger_message)


def init_error_caches(fleet: Fleet) -> None:
    """
    Initialize error caches
    :param fleet:
    """

    if cache.get(CACHE_KEY_FLEET_CHANGED_ERROR + str(fleet.fleet_id)) is None:
        cache.set(CACHE_KEY_FLEET_CHANGED_ERROR + str(fleet.fleet_id), "0", 75)

    if cache.get(CACHE_KEY_NO_FLEET_ERROR + str(fleet.fleet_id)) is None:
        cache.set(CACHE_KEY_NO_FLEET_ERROR + str(fleet.fleet_id), "0", 75)

    if cache.get(CACHE_KEY_NOT_IN_FLEET_ERROR + str(fleet.fleet_id)) is None:
        cache.set(CACHE_KEY_NOT_IN_FLEET_ERROR + str(fleet.fleet_id), "0", 75)

    if cache.get(CACHE_KEY_NO_FLEETBOSS_ERROR + str(fleet.fleet_id)) is None:
        cache.set(CACHE_KEY_NO_FLEETBOSS_ERROR + str(fleet.fleet_id), "0", 75)


@shared_task(**{**TASK_DEFAULT_KWARGS, **{"base": QueueOnce}})
def check_fleet_adverts():
    """
    Scheduled task :: Check for fleets adverts
    """

    required_scopes = ["esi-fleets.read_fleet.v1", "esi-fleets.write_fleet.v1"]
    fleets = Fleet.objects.all()
    fleet_count = fleets.count()

    processing_text = "Processing..." if fleet_count > 0 else "Nothing to do..."

    logger.info(f"{fleet_count} registered fleets found. {processing_text}")

    if fleet_count > 0:
        for fleet in fleets:
            fleet_id = fleet.fleet_id
            fleet_name = fleet.name
            fleet_commander = fleet.fleet_commander
            init_error_caches(fleet=fleet)

            logger.info(
                f'Processing information for fleet "{fleet_name}" '
                f"of {fleet_commander} (ESI ID: {fleet_id})"
            )

            try:
                esi_token = Token.get_token(
                    fleet.fleet_commander.character_id, required_scopes
                )
                fleet_from_esi = esi.client.Fleets.get_characters_character_id_fleet(
                    character_id=esi_token.character_id,
                    token=esi_token.valid_access_token(),
                ).result()
            except HTTPNotFound:
                esi_fleetadvert_error_handling(
                    cache_key=CACHE_KEY_NOT_IN_FLEET_ERROR,
                    fleet=fleet,
                    logger_message=(
                        "FC is not in the registered fleet anymore or fleet is no "
                        "longer available."
                    ),
                )
            except Exception:
                esi_fleetadvert_error_handling(
                    cache_key=CACHE_KEY_NO_FLEET_ERROR,
                    fleet=fleet,
                    logger_message="Registered fleet is no longer available.",
                )

            # We have a valid fleet result from ESI
            else:
                if fleet_id == fleet_from_esi["fleet_id"]:
                    # Check if we deal with the fleet boss here
                    try:
                        _ = esi.client.Fleets.get_fleets_fleet_id_members(
                            fleet_id=fleet_from_esi["fleet_id"],
                            token=esi_token.valid_access_token(),
                        ).result()
                    except Exception:
                        esi_fleetadvert_error_handling(
                            cache_key=CACHE_KEY_NO_FLEETBOSS_ERROR,
                            fleet=fleet,
                            logger_message="FC is no longer the fleet boss.",
                        )
                else:
                    esi_fleetadvert_error_handling(
                        cache_key=CACHE_KEY_FLEET_CHANGED_ERROR,
                        fleet=fleet,
                        logger_message="FC switched to another fleet",
                    )


@shared_task
def get_fleet_composition(fleet_id):
    """
    Getting the fleet composition
    :param fleet_id:
    :return:
    """

    required_scopes = ["esi-fleets.read_fleet.v1", "esi-fleets.write_fleet.v1"]
    fleet = Fleet.objects.get(fleet_id=fleet_id)
    token = Token.get_token(fleet.fleet_commander.character_id, required_scopes)
    fleet_infos = esi.client.Fleets.get_fleets_fleet_id_members(
        fleet_id=fleet_id, token=token.valid_access_token()
    ).result()

    characters = {}
    systems = {}
    ship_type = {}

    for member in fleet_infos:
        characters[member["character_id"]] = ""
        systems[member["solar_system_id"]] = ""
        ship_type[member["ship_type_id"]] = ""

    ids = []
    ids.extend(list(characters.keys()))
    ids.extend(list(systems.keys()))
    ids.extend(list(ship_type.keys()))

    ids_to_name = esi.client.Universe.post_universe_names(ids=ids).result()

    for member in fleet_infos:
        index_character = [x["id"] for x in ids_to_name].index(member["character_id"])
        member["character_name"] = ids_to_name[index_character]["name"]

        index_solar_system = [x["id"] for x in ids_to_name].index(
            member["solar_system_id"]
        )
        member["solar_system_name"] = ids_to_name[index_solar_system]["name"]

        index_ship_type = [x["id"] for x in ids_to_name].index(member["ship_type_id"])
        member["ship_type_name"] = ids_to_name[index_ship_type]["name"]

    aggregate = get_fleet_aggregate(fleet_infos)

    return FleetViewAggregate(fleet_infos, aggregate)


@shared_task
def get_fleet_aggregate(fleet_infos):
    """
    Getting numbers for fleet composition
    :param fleet_infos:
    :return:
    """

    counts = {}

    for member in fleet_infos:
        type_ = member.get("ship_type_name")

        if type_ in counts:
            counts[type_] += 1
        else:
            counts[type_] = 1

    return counts


class FleetViewAggregate:  # pylint: disable=too-few-public-methods
    """
    Helper class
    """

    def __init__(self, fleet, aggregate):
        self.fleet = fleet
        self.aggregate = aggregate
