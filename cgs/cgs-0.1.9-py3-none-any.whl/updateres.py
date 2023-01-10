# updating
from pprint import pprint
import requests
from bs4 import BeautifulSoup


def login_update(username, password, uid, scheduleId, resourceId, day, starthour, endhour, referenceNumber, verbose=False, proxies=None):
    login_data = {
        'email': username,
        'password': password,
        'login': 'submit',
        'resume': ''
    }
    with requests.session() as session:
        login_response = session.post('https://scop-sas.csfoy.ca/booked_sas/Web/index.php', data=login_data, proxies=proxies)
        

        login_soup = BeautifulSoup(login_response.text, features='html.parser')
        csrf = login_soup.find('input', id='csrf_token').get('value')
        if verbose:
            print(f"csrf: {csrf}")

        # after getting the token, let's get the reservationId by viewing the reservation the ref number page response
        view_ref_num = session.get(url=f'https://scop-sas.csfoy.ca/booked_sas/Web/reservation.php?rn={referenceNumber}')
        # pprint(view_ref_num.text)

        find_resid_soup = BeautifulSoup(view_ref_num.text, features='html.parser')
        reservationId = find_resid_soup.find('input', {'name':'reservationId'}).get('value')
        if verbose:
            print(f"reservationId: {reservationId}")

        posturl = "https://scop-sas.csfoy.ca/booked_sas/Web/ajax/reservation_update.php"
        payload = {
        'userId': uid,
        'scheduleId': scheduleId, # the sport id
        'resourceId': resourceId,
        'beginDate': day,
        'beginPeriod': starthour,
        'endDate': day,
        'endPeriod': endhour,
        'reservationTitle': '',
        'reservationDescription': '', 
        'reservationId': reservationId,
        'referenceNumber': referenceNumber,
        'reservationAction': 'update',
        'seriesUpdateScope': 'full', 
        'CSRF_TOKEN': csrf   
        }

        response = session.post(url=posturl, data=payload, proxies=proxies)
        if verbose:
            pprint(response.text)
        post_soup = BeautifulSoup(response.text, features='html.parser')
        try:
            success_msg = post_soup.find('div', id='created-message')
            print("\033[92m"+success_msg.get_text()+"\033[0m")
        except:
            error_msg = post_soup.find('div', id='failed-message').get_text()
            error_reason = post_soup.find('div', class_='error').get_text()
            print("\033[91m" + str(error_msg) + "\n" + "\033[93m" + str(error_reason)+"\033[0m")
        