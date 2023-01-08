import pytest
from django.urls import reverse
from bs4 import BeautifulSoup


@pytest.mark.django_db
def test_view(client, django_user_model):
    django_user_model.objects.create_user(
        username='test', email='test@...', password='top_secret')
    client.login(username='test', password='top_secret')
    response = client.get(reverse('user_home'))
    soup = BeautifulSoup(response.content, 'html.parser')
    token = soup.select('#token')
    assert len(token) == 1
    assert len(token[0].contents[0]) == 40
    assert response.status_code == 200
