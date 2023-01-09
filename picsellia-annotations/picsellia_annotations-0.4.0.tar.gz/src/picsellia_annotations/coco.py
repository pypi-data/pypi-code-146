from typing import Dict, List, Tuple, Union

from pydantic import BaseModel


class Info(BaseModel):
    year: str = None
    version: str = None
    description: str = None
    contributor: str = None
    url: str = None
    date_created: str = None


class Image(BaseModel):
    id: int
    file_name: str
    width: int = None
    height: int = None
    license: int = None
    flickr_url: str = None
    coco_url: str = None
    date_captured: str = None


class License(BaseModel):
    id: int
    name: str
    url: str = None


class Category(BaseModel):
    id: int
    name: str
    supercategory: str = None


class Annotation(BaseModel):
    id: int
    image_id: int
    category_id: int
    bbox: Union[
        Tuple[
            Union[int, float], Union[int, float], Union[int, float], Union[int, float]
        ],
        List,
    ]
    segmentation: Union[List[List[Union[int, float]]], Dict]
    score: float = 0.0
    iscrowd: int = 0

    def area(self) -> float:
        if self.bbox is None or self.bbox == []:
            raise ValueError("This annotation has no bbox, so it does not have area")
        return self.bbox[2] * self.bbox[3]

    def is_rle(self) -> bool:
        return (
            self.segmentation is not None
            and isinstance(self.segmentation, Dict)
            and self.segmentation != {}
        )

    def is_polygon(self) -> bool:
        return (
            not self.is_rle()
            and self.segmentation is not None
            and isinstance(self.segmentation, List)
            and self.segmentation != []
        )

    def is_rectangle(self) -> bool:
        return (
            not self.is_rle()
            and not self.is_polygon()
            and (
                self.segmentation is None
                or self.segmentation == {}
                or self.segmentation == []
            )
            and not self.bbox == []
        )

    def polygon_to_list_coordinates(self) -> List[List[List[int]]]:
        if not self.is_polygon():
            raise ValueError("This is not a polygon")

        k = 0
        polygons = []
        for polygon in self.segmentation:
            if len(polygon) % 2 != 0:
                raise ValueError(
                    f"The {k} element of this segmentation is not a polygon."
                )
            polygons.append(
                [
                    [int(polygon[k]), int(polygon[k + 1])]
                    for k in range(0, len(polygon), 2)
                ]
            )
            k += 1

        return polygons


class COCOFile(BaseModel):
    info: Info = Info()
    licenses: List[License] = []
    categories: List[Category] = []
    images: List[Image]
    annotations: List[Annotation]
