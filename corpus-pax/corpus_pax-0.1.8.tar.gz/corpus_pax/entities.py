import sqlite3

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

    @classmethod
    def associate(cls, tbl: Table, tbl_id: str, area_list: list[str]):
        """For each area in `area_list`, add a row to an m2m table.
        The two tables joined will be the `tbl` parameter and
        `pax_tbl_areas`.
        """
        for area in area_list:
            tbl.update(tbl_id).m2m(
                other_table=cls.__tablename__,
                lookup=cls(**{"area": area}).dict(),
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

    @classmethod
    def associate(cls, tbl: Table, tbl_id: str, category_list: list[str]):
        """For each category in `category_list`, add a row to an m2m table.
        The two tables joined will be the `tbl` parameter and
        `pax_tbl_categories`.
        """
        for category in category_list:
            tbl.update(tbl_id).m2m(
                other_table=cls.__tablename__,
                lookup=cls(**{"category": category}).dict(),
            )


class Individual(RegisteredMember, IndividualBio, TableConfig):
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
    def make_or_replace(
        cls,
        c: Connection,
        url: str,
        replace_img: bool = False,
    ):
        indiv_data = cls.from_url(url, replace_img)
        tbl = c.table(cls)
        row = tbl.insert(indiv_data.dict(), replace=True, pk="id")  # type: ignore
        if pk := row.last_pk:
            if indiv_data.areas:
                PracticeArea.associate(tbl, pk, indiv_data.areas)
            if indiv_data.categories:
                PersonCategory.associate(tbl, pk, indiv_data.categories)


class Org(RegisteredMember, TableConfig):
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
    def make_or_replace(
        cls,
        c: Connection,
        url: str,
        replace_img: bool = False,
    ):
        org_data = cls.from_url(url, replace_img)
        tbl = c.table(cls)
        row = tbl.insert(org_data.dict(), replace=True, pk="id")  # type: ignore
        if pk := row.last_pk:
            if org_data.areas:
                PracticeArea.associate(tbl, pk, org_data.areas)
            if org_data.categories:
                PersonCategory.associate(tbl, pk, org_data.categories)
        org_data.set_membership_rows(c)


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
        sql = "update_member_id_on_insert_email.sql"
        return c.db.execute(
            persons_env.get_template(sql).render(
                membership_tbl=cls.__tablename__,
                individual_tbl=Individual.__tablename__,
            )
        )
