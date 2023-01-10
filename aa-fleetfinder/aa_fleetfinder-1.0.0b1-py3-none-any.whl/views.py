"""
Views
"""

# Third Party
from bravado.exception import HTTPNotFound

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.eveonline.evelinks.eveimageserver import character_portrait_url
from allianceauth.eveonline.models import EveCharacter
from allianceauth.groupmanagement.models import AuthGroup
from allianceauth.services.hooks import get_extension_logger
from esi.decorators import token_required

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Fleet Finder
from fleetfinder import __title__
from fleetfinder.models import Fleet
from fleetfinder.tasks import get_fleet_composition, open_fleet, send_fleet_invitation

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required()
@permission_required("fleetfinder.access_fleetfinder")
def dashboard(request):
    """
    Dashboard view
    :param request:
    :return:
    """

    context = {}

    logger.info(f"Module called by {request.user}")

    return render(request, "fleetfinder/dashboard.html", context)


@login_required()
@permission_required("fleetfinder.access_fleetfinder")
def ajax_dashboard(request) -> JsonResponse:
    """
    Ajax :: Dashboard information
    :param request:
    :return:
    """

    data = []
    groups = request.user.groups.all()
    fleets = Fleet.objects.filter(Q(groups__group__in=groups) | Q(groups=None)).all()

    for fleet in fleets:
        fleet_commander_name = fleet.fleet_commander.character_name
        fleet_commander_portrait_url = character_portrait_url(
            character_id=fleet.fleet_commander.character_id, size=32
        )
        fleet_commander_portrait = (
            '<img class="img-rounded eve-character-portrait" '
            f'src="{fleet_commander_portrait_url}" '
            f'alt="{fleet_commander_name}">'
        )
        fleet_commander_html = fleet_commander_portrait + fleet_commander_name

        button_join_url = reverse("fleetfinder:join_fleet", args=[fleet.fleet_id])
        button_join_text = _("Join Fleet")
        button_join = (
            f'<a href="{button_join_url}" '
            f'class="btn btn-sm btn-default">{button_join_text}</a>'
        )

        button_details = ""
        button_edit = ""

        if request.user.has_perm("fleetfinder.manage_fleets"):
            button_details_url = reverse(
                "fleetfinder:fleet_details", args=[fleet.fleet_id]
            )
            button_details_text = _("View Fleet Details")
            button_details = (
                f'<a href="{button_details_url}" '
                f'class="btn btn-sm btn-default">{button_details_text}</a>'
            )

            button_edit_url = reverse("fleetfinder:edit_fleet", args=[fleet.fleet_id])
            button_edit_text = _("Edit Fleet Advert")
            button_edit = (
                f'<a href="{button_edit_url}" '
                f'class="btn btn-sm btn-default">{button_edit_text}</a>'
            )

        data.append(
            {
                "fleet_commander": {
                    "html": fleet_commander_html,
                    "sort": fleet_commander_name,
                },
                "fleet_name": fleet.name,
                "created_at": fleet.created_at,
                "join": button_join,
                "details": button_details,
                "edit": button_edit,
            }
        )

    return JsonResponse(data, safe=False)


@login_required()
@permission_required("fleetfinder.manage_fleets")
@token_required(scopes=("esi-fleets.read_fleet.v1", "esi-fleets.write_fleet.v1"))
def create_fleet(request, token):
    """
    Create fleet view
    :param request:
    :param token:
    :return:
    """

    if request.method == "POST":
        auth_groups = AuthGroup.objects.filter(internal=False).all()

        context = {}

        if "modified_fleet_data" in request.session:
            context["error"] = request.session["modified_fleet_data"].get("error", "")
            context["motd"] = request.session["modified_fleet_data"].get("motd", "")
            context["name"] = request.session["modified_fleet_data"].get("name", "")
            context["groups"] = request.session["modified_fleet_data"].get("groups", "")
            context["is_free_move"] = request.session["modified_fleet_data"].get(
                "free_move", ""
            )
            context["character_id"] = token.character_id
            context["auth_groups"] = auth_groups

            del request.session["modified_fleet_data"]
        else:
            context = {"character_id": token.character_id, "auth_groups": auth_groups}

        logger.info(f"Fleet created by {request.user}")

        return render(request, "fleetfinder/create-fleet.html", context=context)

    return redirect("fleetfinder:dashboard")


@login_required()
@permission_required("fleetfinder.manage_fleets")
def edit_fleet(request, fleet_id):
    """
    Fleet edit view
    :param request:
    :param fleet_id:
    :return:
    """

    fleet = Fleet.objects.get(fleet_id=fleet_id)
    auth_groups = AuthGroup.objects.filter(internal=False)

    context = {
        "character_id": fleet.fleet_commander.character_id,
        "auth_groups": auth_groups,
        "fleet": fleet,
    }

    logger.info(f"Fleet {fleet_id} edit view by {request.user}")

    return render(request, "fleetfinder/edit-fleet.html", context=context)


@login_required()
@permission_required("fleetfinder.access_fleetfinder")
def join_fleet(request, fleet_id):
    """
    Join fleet view
    :param request:
    :param fleet_id:
    :return:
    """

    context = {}
    groups = request.user.groups.all()
    fleet = Fleet.objects.filter(
        Q(groups__group__in=groups) | Q(groups=None), fleet_id=fleet_id
    ).count()

    if fleet == 0:
        return redirect("fleetfinder:dashboard")

    if request.method == "POST":
        character_ids = request.POST.getlist("character_ids", [])
        send_fleet_invitation.delay(character_ids, fleet_id)

        return redirect("fleetfinder:dashboard")

    characters = (
        EveCharacter.objects.filter(character_ownership__user=request.user)
        .select_related()
        .order_by("character_name")
    )

    context["characters"] = characters

    return render(request, "fleetfinder/join-fleet.html", context=context)


@login_required()
@permission_required("fleetfinder.manage_fleets")
def save_fleet(request):
    """
    Save fleet
    :param request:
    :return:
    """

    if request.method == "POST":
        free_move = request.POST.get("free_move", False)

        if free_move == "on":
            free_move = True

        motd = request.POST.get("motd", "")
        name = request.POST.get("name", "")
        groups = request.POST.getlist("groups", [])

        try:
            open_fleet(request.POST["character_id"], motd, free_move, name, groups)
        except HTTPNotFound as ex:
            if request.POST.get("origin", "") == "edit":
                # Here ccp returns "character not in fleet".
                # Instead, push our own message to be clearer
                messages.error(
                    request,
                    mark_safe(
                        _("<h4>Error!</h4><p>Fleet advert is no longer valid</p>")
                    ),
                )

                return redirect("fleetfinder:dashboard")

            if request.POST.get("origin", "") == "create":
                request.session["modified_fleet_data"] = {
                    "error": ex.swagger_result["error"],
                    "motd": motd,
                    "name": name,
                    "free_move": free_move,
                    "groups": groups,
                }

                return redirect("fleetfinder:create_fleet")

    return redirect("fleetfinder:dashboard")


@login_required()
@permission_required("fleetfinder.manage_fleets")
def fleet_details(request, fleet_id):
    """
    Fleet details view
    :param request:
    :param fleet_id:
    :return:
    """

    context = {"fleet_id": fleet_id}

    logger.info(f"Fleet {fleet_id} details view called by {request.user}")

    return render(request, "fleetfinder/fleet-details.html", context=context)


@login_required()
@permission_required("fleetfinder.manage_fleets")
def ajax_fleet_details(request, fleet_id) -> JsonResponse:
    """
    Ajax :: Fleet Details
    :param request:
    :param fleet_id:
    """

    fleet = get_fleet_composition(fleet_id)

    data = {"fleet_member": [], "fleet_composition": []}

    for member in fleet.fleet:
        data["fleet_member"].append(member)

    for ship, number in fleet.aggregate.items():
        data["fleet_composition"].append({"ship_type_name": ship, "number": number})

    return JsonResponse(data, safe=False)


@register.filter
def get_item(dictionary, key):
    """
    Little helper: get a key from a dictionary
    :param dictionary:
    :param key:
    :return:
    """

    return dictionary.get(key)
