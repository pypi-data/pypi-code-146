from sqlpyd import Connection

from .articles import Article
from .entities import Individual, Org, OrgMember
from .utils import delete_tables_with_prefix


def init_person_tables(c: Connection) -> Connection:
    """Create tables related to persons, i.e. individuals,
    organizations, articles."""

    c.create_table(Individual)
    c.create_table(Org)
    c.create_table(OrgMember)
    OrgMember.on_insert_add_member_id(c)  # add a trigger
    c.create_table(Article)
    c.db.index_foreign_keys()  # auto-generate indexes on fks
    return c


def add_individuals_from_api(c: Connection, replace_img: bool = False):
    """Add/replace records of individuals from an API call."""
    for entity_individual in Individual.list_members_repo():
        Individual.make_or_replace(c, entity_individual["url"], replace_img)


def add_organizations_from_api(c: Connection, replace_img: bool = False):
    """Add/replace records of organizations from an API call."""
    for entity_org in Org.list_orgs_repo():
        Org.make_or_replace(c, entity_org["url"], replace_img)


def add_articles_from_api(c: Connection):
    """Add/replace records of articles from an API call."""
    for extracted_data in Article.extract_articles():
        Article.make_or_replace(c, extracted_data)


def setup_pax(db_path: str, replace_img: bool = False) -> Connection:
    """Recreates tables and populates the same."""
    c = Connection(DatabasePath=db_path, WAL=True)
    delete_tables_with_prefix(c, ["pax"])
    init_person_tables(c)
    add_individuals_from_api(c, replace_img)
    add_organizations_from_api(c, replace_img)
    add_articles_from_api(c)
    return c
