import logging
import random
import secrets
from base64 import b64decode

import requests


from eokulapi.Models.AbsenteeismContainer import AbsenteeismContainer
from eokulapi.Models.AdditionalExam import AdditionalExam
from eokulapi.Models.AvgMarkContainer import AvgMarkContainer
from eokulapi.Models.DocumentContainer import DocumentContainer
from eokulapi.Models.EndtermMarkContainer import EndtermMarkContainer
from eokulapi.Models.EokulStudent import EokulStudent
from eokulapi.Models.ExamScheduleContainer import ExamScheduleContainer
from eokulapi.Models.LessonSchedule import LessonSchedule
from eokulapi.Models.MarkContainer import MarkContainer
from eokulapi.Models.Responsibility import Responsibility
from eokulapi.Models.Transfer import Transfer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

api = "https://e-okul.meb.gov.tr/mobileokulv2"
"""API base URL"""
api_fixed_password = "2^Wd@FJhzWyaf&CE;47RY$.z>=.7~E>w"
"""Fixed password for API requests"""
user_agent = "Dart/2.8 (dart:io)"
"""User-Agent header for API requests"""
app_version = "2.0.12"
"""App version for API requests"""

routes = {
    "register": "/CihazKayit",
    "add_student": "/OgrenciEkle",
    "login_student": "/OgrenciGiris",
    "marks": "/NotBilgileri",
    "absenteeism": "/Devamsizlik",
    "lesson_schedule": "/DersProgrami",
    "exam_schedule": "/SinavTarihleri",
    "avg_marks": "/SubeYaziliOrtalamalari",
    "endterm_marks": "/YilSonuNotlari",
    "transfer": "/NakilBilgisi",
    "responsibibility": "/SorumlulukOys",
    "documents": "/AldigiBelgeler",
    "additional_exam": "/SinavBilgileri",
}
"""API endpoints"""


class EokulAPI:
    """Eokul API wrapper"""

    def __init__(self, uid: str = "None") -> None:
        """Initiates EokulAPI object

        Args:
            uid (str, optional): uid of the EokulAPI user. Auto generated if not given".
        """
        if not uid:
            uid = self.__uid_generator()
        self.uid = uid
        self.gid = None
        self.__logger = logging.getLogger(__name__)
        self.student_dict: dict[str, EokulStudent] = {}
        self.session = requests.session()
        self.session.hooks = dict(response=self.__hook)
        self._update_student_list()

    def __register(self) -> dict:
        """Registers the user to the API"""
        resp = self.session.post(
            url=api + routes["register"],
            headers=self.__header_generator(),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "p": app_version,
                "pid": "",
            },
        )

        self.gid = resp.json()["GID"]
        return resp.json()

    def add_student(
        self, tckn: str, okulno: int, seri: str = "", cilt: str = "", aile: str = ""
    ) -> None:
        """Adds a student to the user

        Args:
            tckn (str): Turkish Citizen ID Number of the student
            okulno (int): School number of the student
            seri (str, optional): `Serial` number of the student. Defaults to "".
            cilt (str, optional): `Cilt` number of the student. Defaults to "".
            aile (str, optional): `Aile` number of the student. Defaults to "".

        Raises:
            AssertionError: If given arguments is not enough
        """
        if seri:
            aile = "yeniKimlik"
            cilt = "yeniKimlik"
        else:
            assert cilt, "cilt no cannot empty if seri is not given"
            assert aile, "aile cannot empty if seri is not given"
            seri = "eskiKimlik"

        pushid = self.__pushid_generator()
        resp = self.session.post(
            url=api + routes["add_student"],
            headers=self.__header_generator(),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
                "tckn": tckn,
                "okulNo": str(okulno),
                "aileSiraNo": aile,
                "ciltNo": cilt,
                "seriNo": seri,
                "kimlikTipi": "0" if seri == "eskiKimlik" else "1",
                "ip": "1.1.1.1",  # bu ne acaba
                "push_id": pushid,
            },
        )
        self._update_student_list()

    def _update_student_list(self) -> None:
        """Updates the student list"""
        data = self.__register()
        self.student_dict.clear()
        for student in data["OgrenciListesi"]:
            login = self.__student_login(student["Tckn"])
            self.student_dict[student["Tckn"]] = (
                EokulStudent(
                    student["Tckn"],
                    student["AdSoyad"],
                    login["Sinif"],
                    login["SinifNo"],
                    login["Numarasi"],
                    b64decode(student["Fotograf"]),
                ),
                login["OgrenciToken"],
            )

    def __get_token(self, student: EokulStudent) -> str:
        """Gets the token of the student

        Args:
            student (EokulStudent): Student object

        Returns:
            str: Token of the student
            "": If the student is not found
        """
        token_list = [token for tckn, (st, token) in self.student_dict.items() if st == student]
        if len(token_list) == 1:
            return token_list[0]
        return ""

    @property
    def students(self) -> list[EokulStudent]:
        """List of the students"""
        return [st for tckn, (st, token) in self.student_dict.items()]

    def update_student_data(self, student: EokulStudent) -> None:
        """Updates all the data of the student

        Args:
            student (EokulStudent): Student object to update
        """
        self._update_marks(student)
        self._update_absenteeism(student)
        self._update_lesson_schedule(student)
        self._update_exam_schedule(student)
        self._update_class_exam_average(student)
        self._update_endterm_marks(student)
        self._update_transfer(student)
        self._update_responsibility(student)
        self._update_documents(student)
        self._update_additional_exams(student)

    def _update_marks(self, student: EokulStudent) -> dict:
        """Updates the marks of the student

        Args:
            student (EokulStudent): Student object to update
        """
        resp = self.session.post(
            url=api + routes["marks"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.marks = MarkContainer.from_dict(resp.json())
        return resp.json()

    def _update_absenteeism(self, student: EokulStudent) -> dict:
        """Updates the absenteeism information of the student

        Args:
            student (EokulStudent): Student object to update
        """
        resp = self.session.post(
            url=api + routes["absenteeism"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.absenteeism = AbsenteeismContainer.from_dict(resp.json())
        return resp.json()

    def _update_lesson_schedule(self, student: EokulStudent) -> dict:
        """Updates the lesson schedule of the student

        Args:
            student (EokulStudent): Student object to update
        """
        resp = self.session.post(
            url=api + routes["lesson_schedule"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.lesson_schedule = LessonSchedule.from_dict(resp.json())
        return resp.json()

    def _update_exam_schedule(self, student: EokulStudent) -> dict:
        """Updates the exam schedule of the student

        Args:
            student (EokulStudent): Student object to update
        """
        resp = self.session.post(
            url=api + routes["exam_schedule"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.exam_schedule = ExamScheduleContainer.from_dict(resp.json())
        return resp.json()

    def _update_class_exam_average(self, student: EokulStudent) -> dict:
        """Updates the class exam average of the student

        Args:
            student (EokulStudent): Student object to update
        """
        resp = self.session.post(
            url=api + routes["avg_marks"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.class_exam_average = AvgMarkContainer.from_dict(resp.json())
        return resp.json()

    def _update_endterm_marks(self, student: EokulStudent) -> dict:
        """Updates the endterm marks of the student

        Args:
            student (EokulStudent): Student object to update
        """
        resp = self.session.post(
            url=api + routes["endterm_marks"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.endterm_marks = EndtermMarkContainer.from_dict(resp.json())
        return resp.json()

    def _update_transfer(self, student: EokulStudent) -> dict:
        """Not implemented method that updates the transfer information of the student

        Args:
            student (EokulStudent): Student object to update
        """

        self.__logger.debug("%s is not implemented", "transfer")
        return {"error": "not implemented"}
        resp = self.session.post(
            url=api + routes["transfer"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.transfer = Transfer.from_dict(resp.json())
        return resp.json()

    def _update_responsibility(self, student: EokulStudent) -> dict:
        """Not implemented method that updates the responsibility information of the student

        Args:
            student (EokulStudent): Student object to update
        """
        self.__logger.debug("%s is not implemented", "responsibility")
        return {"error": "not implemented"}
        resp = self.session.post(
            url=api + routes["responsibility"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.responsibility = Responsibility.from_dict(resp.json())
        return resp.json()

    def _update_documents(self, student: EokulStudent) -> dict:
        """Updates the documents of the student

        Args:
            student (EokulStudent): Student object to update
        """
        resp = self.session.post(
            url=api + routes["documents"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.documents = DocumentContainer.from_dict(resp.json())
        return resp.json()

    def _update_additional_exams(self, student: EokulStudent) -> dict:
        """Updates the additional exams of the student

        Args:
            student (EokulStudent): Student object to update
        """
        resp = self.session.post(
            url=api + routes["additional_exam"],
            headers=self.__header_generator(self.__get_token(student)),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
                "sinifNo": str(student.grade),
            },
        )
        student.additionalexams = AdditionalExam.from_dict(resp.json())
        return resp.json()

    def __student_login(self, tckn: int) -> dict:
        """Logs in the student with the given Identity Number

        Args:
            tckn (int): Identity Number of the student

        Returns:
            dict: Response of the login request that contains the student token
        """

        resp = self.session.post(
            url=api + routes["login_student"],
            headers=self.__header_generator(),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
                "tckn": str(tckn),
                "mobile_platform": "android",
            },
        )
        return resp.json()

    def __pushid_generator(self) -> str:
        """Not implemented method that is supposed to generate a pushid

        Returns:
            str: Pushid
        """
        raise NotImplementedError("we dont know how pushid generated")

    @staticmethod
    def __header_generator(bearer: str = "") -> dict[str, str]:
        """Generates the headers for the requests

        Args:
            bearer (str, optional): Bearer token for the request. Defaults to "".

        Returns:
            dict[str, str]: Headers
        """
        header = {
            "User-Agent": user_agent,
            "Content-Type": "application/json; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Host": "e-okul.meb.gov.tr",
            "Connection": "close",
        }
        if bearer:
            header["Authorization"] = f"Bearer {bearer}"
        return header

    @staticmethod
    def __uid_generator() -> str:
        """Generates a random uid

        Returns:
            str: uid
        """
        rand = random.SystemRandom()
        uid = f"{secrets.token_hex(16)}-{rand.randint(0,1000000000):09d}-{rand.randint(0,1000000000):09d}-{rand.randint(0,1000000):06d}"
        return uid

    def __hook(self, resp: requests.Response, *args, **kwargs):
        """Hook for the requests that handles token refresh actions and errors"""
        if resp.status_code == requests.codes.unauthorized or (
            "ExceptionMessage" in resp.json()
            and resp.json()["ExceptionMessage"]
            == "Object reference not set to an instance of an object."
        ):
            self.__logger.info("student token expired, refreshing")
            student_list = [
                (tckn, st, token)
                for tckn, (st, token) in self.student_dict.items()
                if "Bearer " + token == resp.request.headers["Authorization"]
            ]
            student = student_list[0][1]
            self._update_student_list()
            req = resp.request
            req.headers["Authorization"] = "Bearer " + self.__get_token(student)
            return self.session.send(req)

        if resp.status_code != requests.codes.ok or resp.json()["DurumKodu"] != requests.codes.ok:
            raise RuntimeError(
                f"""unexpected response {resp}: {resp.json()} at url {resp.request.url} with request headers {resp.request.headers}"""
            )
