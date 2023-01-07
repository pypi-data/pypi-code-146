import sqlite3
from typing import Any

from pydantic import EmailStr, Field, conint, constr, validator
from sqlite_utils.db import Table
from sqlpyd import Connection, IndividualBio, TableConfig

from ._api import gh
from .resources import RegisteredMember, persons_env


class PracticeArea(TableConfig):
    __prefix__ = "pax"
    __tablename__ = "areas"
    area: constr(to_lower=True) = Field(  # type: ignore
        col=str,
        description=(
            "Prelude to a taxonomy of legal practice areas, e.g. Data"
            " Engineering, Family Law, Litigation, etc. When joined with a"
            " NaturalProfile or an ArtificialProfile, enables a m2m lookup"
            " table to determine the areas of specialization of the entity"
            " involved. Relatedly, this is also the tagging mechanism for"
            " the Article model."
        ),
    )


class PersonCategory(TableConfig):
    __prefix__ = "pax"
    __tablename__ = "categories"
    category: constr(to_lower=True) = Field(  # type: ignore
        col=str,
        description=(
            "Prelude to a taxonomy of individual / entity categorization, e.g."
            " Lawyer, Law Firm, Accountant, Programmer, etc. When joined with"
            " a NaturalProfile or an ArtificialProfile, enables a m2m lookup"
            " table to determine the kind of the entity involved."
        ),
    )


class Profile(RegisteredMember):
    @classmethod
    def add_record_with_relations(
        cls, profile_table: Table, profile_record: Any
    ) -> Table:
        row = profile_table.insert(profile_record.dict(), pk="id")  # type: ignore
        if row.last_pk:
            for area in profile_record.areas:
                profile_table.update(row.last_pk).m2m(
                    other_table=PracticeArea.__tablename__,
                    lookup=PracticeArea(**{"area": area}).dict(),
                )
            for category in profile_record.categories:
                profile_table.update(row.last_pk).m2m(
                    other_table=PersonCategory.__tablename__,
                    lookup=PersonCategory(**{"category": category}).dict(),
                )
            return profile_table
        raise Exception("No last `pk` from row just inserted.")


class Individual(Profile, IndividualBio, TableConfig):
    __prefix__ = "pax"
    __tablename__ = "individuals"

    @validator("id", pre=True)
    def lower_cased_id(cls, v):
        return v.lower()

    class Config:
        use_enum_values = True

    @classmethod
    def list_members_repo(cls):
        return gh.fetch_entities("members")

    @classmethod
    def make(cls, c: Connection, url: str, replace_img: bool = False):
        indiv = cls.from_url(url, replace_img)
        cls.add_record_with_relations(c.table(cls), indiv)


class Org(Profile, TableConfig):
    __prefix__ = "pax"
    __tablename__ = "orgs"
    official_name: str = Field(None, max_length=100, col=str, fts=True)

    @classmethod
    def list_orgs_repo(cls):
        return gh.fetch_entities("orgs")

    def set_membership_rows(self, c: Connection) -> Table | None:
        member_list = []
        if self.members:
            for member in self.members:
                email = member.pop("account_email", None)
                if email and (acct := EmailStr(email)):
                    obj = OrgMember(
                        org_id=self.id,
                        individual_id=None,
                        rank=member.get("rank", 10),
                        role=member.get("role", "Unspecified"),
                        account_email=acct,
                    )
                    member_list.append(obj)
        if member_list:
            return c.add_cleaned_records(OrgMember, member_list)
        return None

    @classmethod
    def make(cls, c: Connection, url: str, replace_img: bool = False):
        org = cls.from_url(url, replace_img)
        cls.add_record_with_relations(c.table(cls), org)
        org.set_membership_rows(c)


class OrgMember(TableConfig):
    __prefix__ = "pax"
    __tablename__ = "org_members"
    org_id: str = Field(
        ...,
        title="Org ID",
        description="The Org primary key.",
        col=str,
        fk=(Org.__tablename__, "id"),
    )
    individual_id: str | None = Field(
        None,
        title="Member ID",
        description=(
            "The Natural Person primary key derived from the account email."
        ),
        col=str,
        fk=(Individual.__tablename__, "id"),
    )
    rank: conint(strict=True, gt=0, lt=10) = Field(  # type: ignore
        ...,
        title="Rank in Org",
        description=(
            "Enables ability to customize order of appearance of users within"
            " an organization."
        ),
        col=int,
    )
    role: constr(strict=True, max_length=50) = Field(  # type: ignore
        ...,
        title="Role",
        description=(
            "Descriptive text like 'Managing Partner' or 'Junior Developer',"
            " e.g. the role of the individual person within an organization."
        ),
        col=str,
    )
    account_email: EmailStr = Field(
        ...,
        title="Account Email",
        description=(
            "Lookup the Natural Profile's email to get the individual's id."
        ),
        col=str,
    )

    @classmethod
    def on_insert_add_member_id(cls, c: Connection) -> sqlite3.Cursor:
        """Since the original data doesn't contain the `member id` yet,
        we need to setup up trigger. The trigger will ensure that,
        on insert of a `OrgMember` row, the email address contained in the row
        can be used to fetch the member id and include it in the `OrgMember`
        row just inserted.
        """
        temp = persons_env.get_template("update_member_id_on_insert_email.sql")
        return c.db.execute(
            temp.render(
                membership_tbl=OrgMember.__tablename__,
                individual_tbl=Individual.__tablename__,
            )
        )
