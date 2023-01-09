"""
课程商城
"""
from ..base import base


class courseLibrary(base):
    def __init__(self, token, app_secret=None):
        """course library's init
        Args:
            token (str): cjdg access_token
            app_secret (str, optional): cjdg app_secret. Defaults to None.
        """
        super().__init__(token, app_secret=app_secret)

    def create(self, _id):
        pass

    def list(self):
        pass

    def read(self, _id):
        pass

    def update(self, _id, data):
        pass

    def delete(self, _id):
        pass


class courseSelectLibrary(base):
    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret=app_secret)

    def list(self, course_type_id=None, page=1, rows=20):
        api_name = "coursequerycourseToCheck.jhtml"
        data = {
            # "course.courseType": course_type_id,
            "page": page,
            "rows": rows,
        }
        # logger.debug(data)
        response = self.request(
            api_name=api_name,
            data=data,
            method="POST",
            api_prefix=""
        )
        rows = response.get("rows")
        if rows:
            for row in rows:
                row["course_type_id"] = course_type_id
                yield row

    def create(self, _id):
        pass
