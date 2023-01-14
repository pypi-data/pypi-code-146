from rest_framework.test import APITestCase
from django.urls import reverse
from kfsdutils.apps.endpoints.handlers.core.utils import FileUtils

class EndpointsTestHandler(APITestCase):

    def setUp(self):
        self.__fileUtils = FileUtils()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def readJSONData(self, filepath):
        return self.__fileUtils.readJsonFromFile(filepath)

    def fetchPg(self, listUrl, currentPg):
        if currentPg:
            listUrl = listUrl + "?page={}".format(currentPg)
        return listUrl

    def detailView(self, name, identifier):
        return reverse(name, args=[identifier])

    def createView(self, name):
        return reverse(name)

    def list(self, url, currentPg, expStatus):
        paginatedUrl = self.fetchPg(url, currentPg)
        response = self.client.get(paginatedUrl, format='json')
        self.assertEqual(response.status_code, expStatus, response.data)
        return response

    def get(self, name, identifier, expStatus):
        detailUrl = self.detailView(name, identifier)
        response = self.client.get(detailUrl, format='json')
        self.assertEqual(response.status_code, expStatus, response.data)
        return response

    def create(self, url, data, expStatus):
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, expStatus, response.data)
        responseData = response.data
        if "created" in responseData:
            responseData.pop("created")

        if "updated" in responseData:
            responseData.pop("updated")
        return responseData

    def patch(self, name, identifier, data, expStatus):
        detailUrl = self.detailView(name, identifier)
        response = self.client.patch(detailUrl, data=data, format='json')
        self.assertEqual(response.status_code, expStatus, response.data)
        responseData = response.data
        if "created" in responseData:
            responseData.pop("created")

        if "updated" in responseData:
            responseData.pop("updated")
        return responseData

    def delete(self, name, identifier, expStatus):
        detailUrl = self.detailView(name, identifier)
        response = self.client.delete(detailUrl, format='json')
        self.assertEqual(response.status_code, expStatus, response.data)
        return response

