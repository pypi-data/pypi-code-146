# creating 
from pprint import pprint
import requests
from bs4 import BeautifulSoup


def login_create(username: str, password: str, uid: str, scheduleId: str, resourceId: str, day: str, starthour: str, endhour: str, verbose=False, proxies=None): #must all be strings
    '''login and create a reservation, all params must be strings'''
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

        # after getting the token, let's reserve
        posturl = "https://scop-sas.csfoy.ca/booked_sas/Web/ajax/reservation_save.php"
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
        'reservationId': '',
        'referenceNumber': '',
        'reservationAction': 'create',
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
            ref_num = post_soup.find('div', id="reference-number").get_text().split()[-1]
            if verbose:
                print(f"reference number: {ref_num}")
            return ref_num
        except:
            error_msg = post_soup.find('div', id='failed-message').get_text()
            error_reason = post_soup.find('div', class_='error').get_text()
            print("\033[91m" + str(error_msg) + "\n" + "\033[93m" + str(error_reason)+"\033[0m")
            return None
