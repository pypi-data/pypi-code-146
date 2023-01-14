from datetime import datetime
from uuid import UUID

from severino.sdk.helpers.http_requests import Http
from severino.settings import SEVERINO_API_URL


class VagasDotComBot:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/vagas-dot-com/bot"

    def create(
        self,
        vagas_job_id: str,
        gh_job_id: str,
        last_migration_at: datetime,
    ):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={
                "vagas_job_id": vagas_job_id,
                "gh_job_id": gh_job_id,
                "last_migration_at": last_migration_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

    def read(self, migration_uuid: str):
        return self.http.get(
            url=f"{self.severino_api_url}{self.path}/{migration_uuid}/"
        )

    def list(self, filters: dict = {}):
        """List

        Args:
            filters (dict, optional): List of filters: vagas_job_id, gh_job_id, last_migration_at E.g: {"vagas_job_id": 999999}.

        Returns:
            _type_: _description_
        """
        return self.http.get(url=f"{self.severino_api_url}{self.path}/", params=filters)

    def update(
        self,
        migration_uuid: str,
        vagas_job_id: str = None,
        gh_job_id: str = None,
        last_migration_at: datetime = None,
    ):
        data = {"vagas_job_id": vagas_job_id, "gh_job_id": gh_job_id}

        if last_migration_at:
            data["last_migration_at"] = last_migration_at.strftime("%Y-%m-%d %H:%M:%S")

        data = {key: data[key] for key in data if not key}

        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{migration_uuid}/",
            data=data,
        )

    def delete(self, migration_uuid):
        return self.http.delete(
            url=f"{self.severino_api_url}{self.path}/{migration_uuid}/"
        )


class VagasDotComCandidateMigration:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/vagas-dot-com/candidate-migration"

    def create(
        self,
        migration_uuid: UUID,
        name: str,
        city: str = "",
        most_recent_professional_experience: str = "",
        vagas_candidate_id: str = "",
    ):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={
                "name": name,
                "city": city,
                "most_recent_professional_experience": most_recent_professional_experience,
                "vagas_candidate_id": vagas_candidate_id,
                "migration": migration_uuid,
            },
        )

    def read(self, candidate_migration_uuid: str):
        return self.http.get(
            url=f"{self.severino_api_url}{self.path}/{candidate_migration_uuid}/"
        )

    def list(self, filters: dict = {}):
        """List

        Args:
            filters (dict, optional): List of filters: vagas_candidate_id E.g: {"vagas_candidate_id": "999999"}.

        Returns:
            _type_: _description_
        """
        return self.http.get(url=f"{self.severino_api_url}{self.path}/", params=filters)

    def update(
        self,
        candidate_migration_uuid: UUID,
        migration_uuid: UUID,
        name: str,
        city: str,
        most_recent_professional_experience: str,
        vagas_candidate_id: str,
    ):
        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{candidate_migration_uuid}/",
            data={
                "name": name,
                "city": city,
                "most_recent_professional_experience": most_recent_professional_experience,
                "vagas_candidate_id": vagas_candidate_id,
                "migration": migration_uuid,
            },
        )

    def delete(self, candidate_migration_uuid):
        return self.http.delete(
            url=f"{self.severino_api_url}{self.path}/{candidate_migration_uuid}/"
        )


class VagasDotComCandidateGHLoad:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/vagas-dot-com/candidate-gh-load"

    def create(
        self,
        name: str,
        email: str,
        gh_candidate_id: str,
        status: str,
        vagas_candidate_id: str = None,
    ):
        candidate_migration = {}
        if vagas_candidate_id:
            candidate_migration = (
                VagasDotComCandidateMigration()
                .list(filters={"vagas_candidate_id": vagas_candidate_id})
                .json()
            )

        candidate_migration_uuid = None
        if candidate_migration and candidate_migration.get("count", 0) > 0:
            candidate_migration_uuid = candidate_migration["results"][0]["id"]

        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={
                "candidate_migration": candidate_migration_uuid,
                "name": name,
                "email": email,
                "gh_candidate_id": gh_candidate_id,
                "status": status,
            },
        )

    def read(self, candidate_gh_load_uuid: str):
        return self.http.get(
            url=f"{self.severino_api_url}{self.path}/{candidate_gh_load_uuid}/"
        )

    def list(self, filters: dict = {}):
        """List

        Args:
            filters (dict, optional): List of filters: gh_candidate_id E.g: {"gh_candidate_id": "999999"}.

        Returns:
            _type_: _description_
        """
        return self.http.get(url=f"{self.severino_api_url}{self.path}/", params=filters)

    def update(
        self,
        candidate_gh_load_uuid: UUID,
        candidate_migration_uuid: UUID,
        name: str,
        email: str,
        gh_candidate_id: str,
        status: str,
    ):
        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{candidate_gh_load_uuid}/",
            data={
                "candidate_migration": candidate_migration_uuid,
                "name": name,
                "email": email,
                "gh_candidate_id": gh_candidate_id,
                "status": status,
            },
        )

    def delete(self, candidate_gh_load_uuid):
        return self.http.delete(
            url=f"{self.severino_api_url}{self.path}/{candidate_gh_load_uuid}/"
        )
