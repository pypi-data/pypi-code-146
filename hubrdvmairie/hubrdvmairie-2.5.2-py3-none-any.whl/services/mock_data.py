import random
from datetime import datetime, timedelta


def get_mock_managed_meeting_points(editor):
    if editor.name == "RDV360":
        return [
            {
                "id": "201",
                "name": "Mairie ANNEXE LILLE-SECLIN",
                "longitude": 3.0348016639327,
                "latitude": 50.549140395451,
                "_internal_id": "123123",
                "public_entry_address": "89 RUE ROGER BOUVRY",
                "zip_code": "59113",
                "city_name": "LILLE-SECLIN",
                "website": "http://www.ville-seclin.fr",
                "city_logo": "https://www.ville-seclin.fr/images/logo-ville-seclin/logo_ville_de_seclin.png",
                "_editor_name": "RDV360",
            },
            {
                "id": "202",
                "name": "Mairie de Quartier de Lille-Sud",
                "longitude": 3.0475818403133,
                "latitude": 50.612875943839,
                "internal_id": "456456",
                "public_entry_address": "83 Rue du Faubourg des Postes",
                "zip_code": "59000",
                "city_name": "LILLE-SECLIN",
                "website": "http://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud",
                "city_logo": "https://www.ville-seclin.fr/images/logo-ville-seclin/logo_ville_de_seclin.png",
                "_editor_name": "RDV360",
            },
            {
                "id": "203",
                "name": "Mairie du 10e Arrondissement de Paris",
                "longitude": 2.357828,
                "latitude": 48.8717442,
                "_internal_id": "789879",
                "public_entry_address": "72 Rue du Faubourg Saint-Martin",
                "zip_code": "75010",
                "city_name": "Paris",
                "website": "https://mairie10.paris.fr",
                "city_logo": "https://www.grapheine.com/wp-content/uploads/Plan-de-travail-36paris-logo.jpg",
                "_editor_name": "RDV360",
            },
        ]
    elif editor.name == "OrionRDV":
        return [
            {
                "id": "FF65E",
                "name": "Mairie du 15e Arrondissement de Paris",
                "longitude": 2.2981566,
                "latitude": 48.8414021,
                "_internal_id": "12412315124",
                "public_entry_address": "31 Rue Péclet",
                "zip_code": "75015",
                "city_name": "Paris",
                "website": "https://mairie15.paris.fr",
                "city_logo": "https://www.grapheine.com/wp-content/uploads/Plan-de-travail-36paris-logo.jpg",
                "_editor_name": "OrionRDV",
            },
            {
                "id": "FF33E",
                "name": "Mairie du 18e Arrondissement de Paris",
                "longitude": 2.3303431,
                "latitude": 48.8909042,
                "_internal_id": "67868",
                "public_entry_address": "1 Pl. Jules Joffrin",
                "zip_code": "75018",
                "city_name": "Paris",
                "website": "https://mairie18.paris.fr",
                "city_logo": "https://www.grapheine.com/wp-content/uploads/Plan-de-travail-36paris-logo.jpg",
                "_editor_name": "OrionRDV",
            },
            {
                "id": "FF22E",
                "name": "Mairie du 2e Arrondissement de Paris",
                "longitude": 2.3402125,
                "latitude": 48.866407,
                "_internal_id": "12123345",
                "public_entry_address": "8 Rue de la Banque",
                "zip_code": "75002",
                "city_name": "Paris",
                "website": "https://mairiepariscentre.paris.fr/",
                "city_logo": "https://www.grapheine.com/wp-content/uploads/Plan-de-travail-36paris-logo.jpg",
                "_editor_name": "OrionRDV",
            },
        ]
    elif editor.name == "Ytop":
        return [
            {
                "id": "00342",
                "name": "Mairie du 13e Arrondissement de Paris",
                "longitude": 2.336658,
                "latitude": 48.8486635,
                "_internal_id": "998778",
                "public_entry_address": "1 Pl. d'Italie",
                "zip_code": "75013",
                "city_name": "Paris",
                "website": "https://mairie13.paris.fr/",
                "city_logo": "https://www.grapheine.com/wp-content/uploads/Plan-de-travail-36paris-logo.jpg",
                "_editor_name": "SynBird",
            },
        ]
    else:
        return []


def get_mock_slots(meeting_point, start_date=None, end_date=None):
    slots_list = []
    index = 0
    while index < 50:
        slots_list.append(
            {
                "callback_url": meeting_point["website"] + "/rendez-vous/passeports",
                "datetime": datetime.now().replace(
                    hour=(random.randint(7, 19)), minute=(random.randint(0, 2) * 20)
                )
                + timedelta(days=50 + random.randint(1, 100)),
            }
        )
        if slots_list[-1]["datetime"].weekday() == 6:
            slots_list.pop()
        index += 1

    # filter by dates

    if start_date and end_date:
        filtered_slots_list = []
        start_datetime = datetime.now().replace(
            year=start_date.year,
            month=start_date.month,
            day=start_date.day,
            hour=0,
            minute=0,
            second=0,
        )
        end_datetime = datetime.now().replace(
            year=end_date.year,
            month=end_date.month,
            day=end_date.day,
            hour=23,
            minute=59,
            second=59,
        )

        for slot in slots_list:
            if start_datetime < slot["datetime"] and end_datetime > slot["datetime"]:
                filtered_slots_list.append(slot)
        return filtered_slots_list, None
    else:
        return slots_list, None


def get_mock_slots_multiple(meeting_points, start_date=None, end_date=None):
    slots = {}
    for meeting_point in meeting_points:
        meeting_point_slots = [
            x[0] for x in get_mock_slots(meeting_point, start_date, end_date) if x
        ]
        slots[meeting_point["_internal_id"]] = meeting_point_slots
    print("Slots : " + str(len(slots)))
    return slots, None


def get_mock_slots_with_meeting_point_data(editors_list):
    meeting_points_list = []
    for editor in editors_list:
        meeting_points_list += get_mock_managed_meeting_points(editor)
    for meeting_point in meeting_points_list:
        slots_list = get_mock_slots(meeting_point)
        meeting_point["available_slots"] = slots_list
        meeting_point["distance_km"] = random.uniform(0.3, 10)
    return meeting_points_list


def get_mock_applications(application_ids):
    result = {}
    for application_id in application_ids:
        result[application_id] = [
            {
                "meeting_point": "Mairie du 2e Arrondissement de Paris",
                "datetime": "2022-11-10T10:00Z",
                "management_url": "https://mairiepariscentre.paris.fr/rendez-vous/predemande?num=6123155111",
                "cancel_url": "https://mairiepariscentre.paris.fr/rendez-vous/annulation?num=6123155111",
            },
            {
                "meeting_point": "Mairie du 13e Arrondissement de Paris",
                "datetime": "2022-11-10T16:00Z",
                "management_url": "https://mairie13.paris.fr/rendez-vous/predemande?num=6123155111",
                "cancel_url": "https://mairiepariscentre.paris.fr/rendez-vous/annulation?num=6123155111",
            },
        ]
    return result
