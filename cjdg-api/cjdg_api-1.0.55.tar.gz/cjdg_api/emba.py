from loguru import logger
from .base import base


class emba(base):
    def __init__(self, token):
        super().__init__(token)


class bmsEmba(emba):
    """
    # 管理端接口
    """

    def __init__(self, token):
        super().__init__(token)

    def request(self, **kwarg):
        api_prefix = ""
        headers = {
            "Cookie": f"accessToken={self.token}"
        }
        return super().request(api_prefix=api_prefix,
                               headers=headers,
                               ** kwarg)

    def list(self, book_name=None):
        api_name = "booklistBook.jhtml"
        data = {
            "EB.name": book_name,
        }
        response = self.request(
            api_name=api_name,
            data=data,
            method="POST",
        )
        rows = response.get("rows")
        if rows:
            return rows
        logger.error({
            "msg": "没有查找到书本。",
            "book_name": book_name
        })

    def getBook(self):
        return self.list()

    def get(self, book_id):
        pass

    def get_book_tree(self, book_id):
        api_name = "booktreeBook.jhtml"
        params = {
            "book_id": book_id,
        }
        data = {
        }
        response = self.request(
            api_name=api_name,
            params=params,
            data=data,
            method="POST",
        )
        if response:
            return response[0]
        logger.error({
            "msg": "没有得到书本结构。",
            "book_id": book_id
        })

    def section_list(self, book_id):
        response = self.get_book_tree(book_id=book_id)
        if response:
            section_children = response.get("children")
            for section in section_children:
                yield section

    def section_info(self, section_name, book_id):
        for section in self.section_list(book_id=book_id):
            if section.get("text") == section_name:
                return section
        logger.error({
            "msg": "查找不到此单元名称",
            "section_name": section_name,
        })

    def chapter_list(self, book_id):
        sections = self.section_list(book_id=book_id)
        if sections:
            for section in sections:
                chapters = section.get("children")
                for chapter in chapters:
                    chapter_type = chapter.get("type")
                    if chapter_type == 1:
                        yield chapter

    def chapter_info(self, chapter_name, book_id):
        for chapter in self.chapter_list(book_id=book_id):
            if chapter.get("text") == chapter_name:
                return chapter
        logger.error({
            "msg": "查找不到此章节名称",
            "chapter_name": chapter_name,
        })

    def exam_list(self, book_id):
        sections = self.section_list(book_id=book_id)
        if sections:
            for section in sections:
                exams = section.get("children")
                for exam in exams:
                    chapter_type = exam.get("type")
                    if chapter_type == 2:
                        yield exam

    def exam_info(self, exam_name, book_id):
        for exam in self.exam_list(book_id=book_id):
            if exam.get("text") == exam_name:
                return exam
        logger.error({
            "msg": "查找不到此闯关名称",
            "exam_name": exam_name,
        })

    def lesson_list(self, book_id):
        chapters = self.chapter_list(book_id=book_id)
        if chapters:
            for chapter in chapters:
                lessons = chapter.get("children")
                for lesson in lessons:
                    yield lesson

    def lesson_info(self, lesson_name, book_id):
        for lesson in self.lesson_list(book_id=book_id):
            if lesson.get("text") == lesson_name:
                return lesson
        logger.error({
            "msg": "查找不到此课程名称",
            "lesson_name": lesson_name,
        })

    def add_section(self, book_id, section_name):
        """
        添加单元
        未完成，慎用。
        """
        api_name = "bookaddBook.jhtml"
        params = {
            "level": 0,
            "book_id": book_id,
        }
        data = {
            "ESection.name": section_name,
        }
        response = self.request(
            api_name=api_name,
            params=params,
            data=data,
            method="POST",
        )
        info = response.get("info")
        if info == "ok":
            return response
        logger.error({
            "msg": "添加单元失败",
            "book_id": book_id,
            "section_name": section_name,
        })

    def add_chapter(self, section_id):
        """
        添加章节
        """
        pass

    def add_lesson(self, chapter_id):
        """
        添加课程
        """
        pass

    def add_exam(self, section_id):
        """
        添加考试
        """
        pass


class appEmba(emba):
    """
    # 移动端接口
    """

    def __init__(self, token):
        super().__init__(token)

    def getBookDir(self, book_id):
        api_name = "emba/getBookDir"
        data = {}
        data["book_id"] = book_id
        return self.request(api_name)

    def getCourseList(self, interface_type=3):
        # 书的目录结构
        api_name = "emba/getCourseList"
        data = {}
        data["interface_type"] = interface_type
        return self.request(api_name=api_name, data=data)

    def addTopic(self, data):
        api_name = "activity/addTopic"
        return self.request(api_name, data)
