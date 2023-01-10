from typing import Any
from CxAdmin.api.cxItem import CxItem
from CxAdmin.objects.cxList import CxList
import json


class CxLists(CxItem):
    def getAllLists(self) -> list[CxList]:
        listsJson: str = self._httpClient.get(self._path)
        lists = [
            CxList.from_json(json.loads(thisListJson)["result"])
            for thisListJson in listsJson
        ]
        return lists

    def getList(self, listId: str) -> CxList:
        listJson: str = self._httpClient.get(f"{self._path}/{listId}")
        listItem = CxList.from_json(json.loads(listJson)["result"])
        return listItem

    def uploadListCSV(self, id: str, csv: str) -> dict[str, Any]:
        listJson: dict[str, Any] = self._httpClient.post(
            f"{self._path}/{id}/upload", csv
        )
        return listJson

    def uploadList(self, list: CxList) -> dict[str, Any]:
        return self.uploadListCSV(
            list.id,
            list.constructDataCSV(),
        )

    def getListCSV(self, listId: str) -> Any:
        return self._httpClient.get(f"{self._path}/{listId}/download/list-items.csv")
