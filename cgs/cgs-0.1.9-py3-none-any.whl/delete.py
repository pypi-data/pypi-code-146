from pprint import pprint
import requests
from bs4 import BeautifulSoup


def login_delete(username, password, uid, referenceNumber, proxies=None):
    login_data = {
        'email': username,
        'password': password,
        'login': 'submit',
        'resume': ''
    }
    with requests.session() as session:
        login_response = session.post('https://scop.cegep-ste-foy.qc.ca/booked/Web/index.php', data=login_data, proxies=proxies)
        

        login_soup = BeautifulSoup(login_response.text, features='html.parser')
        csrf = login_soup.find('input', id='csrf_token').get('value')
        print(csrf)

        # after getting the token, let's get the reservationId by viewing the reservation the ref number page response
        view_ref_num = session.get(url=f'https://scop.cegep-ste-foy.qc.ca/booked/Web/reservation.php?rn={referenceNumber}')
        # pprint(view_ref_num.text)

        find_resid_soup = BeautifulSoup(view_ref_num.text, features='html.parser')
        reservationId = find_resid_soup.find('input', {'name':'reservationId'}).get('value')
        print(reservationId)

        posturl = "https://scop.cegep-ste-foy.qc.ca/booked/Web/ajax/reservation_delete.php"
        payload = {
        'userId': uid,
        'scheduleId': '53', # the sport id
        'resourceId': '4252',
        'beginDate': '2022-04-30',
        'beginPeriod': '10:00:00',
        'endDate': '2022-04-30',
        'endPeriod': '11:00:00',
        'reservationTitle': '',
        'reservationDescription': '', 
        'reservationId': reservationId,
        'referenceNumber': referenceNumber,
        'reservationAction': 'update',
        'seriesUpdateScope': 'full', 
        'CSRF_TOKEN': csrf   
        }

        response = session.post(url=posturl, data=payload, proxies=proxies)
        pprint(response.text)
        post_soup = BeautifulSoup(response.text, features='html.parser')
        try:
            success_msg = post_soup.find('div', id='created-message')
            print(success_msg.get_text())
        except:
            error_msg = post_soup.find('div', id='failed-message').get_text()
            error_reason = post_soup.find('div', class_='error').get_text()
            print(str(error_msg) + "\n" + str(error_reason))



# print("ip:", requests.get('http://jsonip.com', proxies=configfile.proxies).json()['ip'])
# login_delete(configfile.username, configfile.password, uid='1200', referenceNumber='62659be0dccee621505359')
