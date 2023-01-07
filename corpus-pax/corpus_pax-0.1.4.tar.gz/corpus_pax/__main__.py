from sqlpyd import Connection

from .articles import Article
from .entities import Individual, Org, OrgMember


def init_person_tables(c: Connection) -> Connection:
    """Create tables related to persons, i.e. individuals, organizations, articles."""

    # creates tables
    c.create_table(Individual)
    c.create_table(Org)
    c.create_table(OrgMember)
    c.create_table(Article)

    # auto-generate indexes on fks
    c.db.index_foreign_keys()

    # add a trigger
    OrgMember.on_insert_add_member_id(c)
    return c


def add_individuals_from_api(c: Connection, replace_img: bool = False):
    """Add records of individuals from an API call."""
    for entity_individual in Individual.list_members_repo():
        Individual.make(c, entity_individual["url"], replace_img)


def add_organizations_from_api(c: Connection, replace_img: bool = False):
    """Add records of organizations from an API call."""
    for entity_org in Org.list_orgs_repo():
        Org.make(c, entity_org["url"], replace_img)


def add_articles_from_api(c: Connection, replace_img: bool = False):
    """Add records of articles from an API call."""
    for extracted_data in Article.extract_articles():
        Article.make(c, extracted_data)


def init_persons(c: Connection, replace_img: bool = False):
    """Creates the tables and populates the same."""
    init_person_tables(c)
    add_individuals_from_api(c, replace_img)
    add_organizations_from_api(c, replace_img)
    add_articles_from_api(c)
