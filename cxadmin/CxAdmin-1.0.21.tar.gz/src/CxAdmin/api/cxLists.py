from typing import Any
from CxAdmin.api.cxItem import CxItem
from CxAdmin.objects.cxList import CxList


class CxLists(CxItem):
    @staticmethod
    def __split_csv(every: int, csv: str) -> list[str]:
        """Helper function to split a csv into chunks of a given size."""
        lines = csv.splitlines()
        # get header row
        header = lines[0]
        # return ["\n".join(lines[i : i + every]) for i in range(0, len(lines), every)]
        return [
            (header + "\n" + "\n".join(lines[i : i + every]))
            for i in range(1, len(lines), every)
        ]

    def getAllLists(self) -> list[CxList]:
        listsJson: list[dict[str, str]] = self._httpClient.get(self._path)
        lists = [CxList.from_json(thisListJson) for thisListJson in listsJson]
        return lists

    def getList(self, listId: str) -> CxList:
        listJson: dict[str, Any] = self._httpClient.get(f"{self._path}/{listId}")  # type: ignore
        listItem = CxList.from_json(listJson)
        return listItem

    def uploadListCSV(self, id: str, csv: str) -> dict[str, Any]:
        listJson: dict[str, Any] = self._httpClient.post(
            f"{self._path}/{id}/upload",
            csv,
            withResultJsonKey=False,
        )
        return listJson

    def uploadList(self, list: CxList) -> dict[str, Any]:
        return self.uploadListCSV(
            list.id,
            list.constructDataCSV(),
        )

    def getListCSV(self, listId: str) -> Any:
        return self._httpClient.get(
            f"{self._path}/{listId}/download/list-items.csv",
            withResultJsonKey=False,
        )
