#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import os.path as osp
import datetime
from poppy.core.logger import logger
import os


from poppy.core.tools.exceptions import print_exception
from poppy.core.db.handlers import get_or_create
from poppy.core.command import Command
from poppy.core.db.database import Database
from roc.guest.models.meb_gse.database import DatabaseInformation
from roc.guest.models.meb_gse_data.test import Descriptor
from roc.guest.models.meb_gse_data.event import Event
from roc.guest.models.meb_gse_data.device import Device
from roc.guest.models.meb_gse_data.parser import ParserCollection
from roc.guest.models.meb_gse_data.packet import PacketType
from roc.guest.meb_connector import MEBSelector
from poppy.pop.tools import paths




def generate_database_information(session, databases):
    """
    Generate the database informations.
    """
    logger.info("Generate the database informations")

    databases = [
        get_or_create(
            session,
            DatabaseInformation,
            DatabaseName=database,
        )
        for database in databases
    ]
    for database in databases:
        database.CreationDate = datetime.datetime.now()
        database.TerminatedDate = datetime.datetime.now()

    database.Current = True


def create_meb_databases(meb, name, number):
    # create the engine of the database
    meb.create_engine()

    # try closing the session to kill all current transactions
    try:
        meb.scoped_session.close_all()
    except Exception as e:
        logger.error("Can't close sessions on sqlalchemy")
        logger.error(e)
        raise e

    # connection
    conn = meb.engine.connect()

    # names for meb data databases
    databases = [
        "{0}_data_{1}".format(name, x) for x in range(1, number + 1)
    ]

    # drop and create all databases
    try:
        logger.info("Creating databases")
        conn.execute("COMMIT")
        conn.execute("DROP DATABASE IF EXISTS {0}".format(name))
        conn.execute("CREATE DATABASE {0}".format(name))

        # read the script
        with open(paths.from_scripts("create_meb.sql"), "r") as f:
            script = f.read()

        # execute the script for database
        conn.execute("USE {0}".format(name))
        conn.execute(script)

        # read the script
        with open(paths.from_scripts("create_meb_data.sql"), "r") as f:
            script = f.read()

        # loop over databases
        for database in databases:
            conn.execute(
                "DROP DATABASE IF EXISTS {0}".format(database)
            )
            conn.execute("CREATE DATABASE {0}".format(database))
            conn.execute("USE {0}".format(database))

            # execute the script
            conn.execute(script)

        #  conn.execute("USE {0}".format(current))
        conn.execute("COMMIT")
    except Exception as e:
        logger.error(e)
        raise e

    # return create databases names
    return databases


def data_to_meb(session, path):
    """
    Transfer the data of test logs presents in the path directory into the fake
    MEB database.
    """
    # loop over files presents recursively in the given path
    for root, dirs, files in os.walk(path):
        for file_ in files:
            if file_.endswith(".xml"):
                xml_to_database(session, osp.join(root, file_))


def xml_to_database(session, xml):
    """
    Open the given XML file and dump its structure into the MEB database.
    """
    # open wml file
    logger.info("Treating file {0}".format(xml))
    with open(xml, "r") as f:
        # list of events
        events = []

        # loop without parsing on the document
        for _, elem in ET.iterparse(f, ["end"]):
            # if this is a TestDescriptor field
            if elem.tag == "TestDescriptor":
                # create a descriptor
                test = create_descriptor(elem)
                session.add(test)
                session.commit()

                # clear the element to not keep the whole document in memory,
                # this really IMPORTANT to not have a lot of memory used for
                # large files to parse
                elem.clear()

            # if this an EventDescr
            elif elem.tag == "EventDescr":
                # create an event
                event = create_event(session, elem, test)
                events.append(event)

                # clear the element
                elem.clear()

        session.add_all(events)


def create_descriptor(node):
    """
    Create a descriptor and add it into memory.
    """
    # execution information
    exec_info = node.find("ExecutionInformation")

    # informations
    info = node.find("GeneralInfo")

    # node for the description
    description = info.find("LongDescription")

    # creation date
    date = info.find("CreationDate")

    test = Descriptor(
        TestName=node.get("TestName"),
        UUID=node.get("TestUUID"),
        Status=exec_info.find("Status").text,
        Author=info.find("Author").text if info.find("Author") else None,
        Description=description.text,
        CreationDate=date.text,
        OneShot=False if node.find("OneShotTestInformation") is None else True,
        Launched=exec_info.find("LaunchedDate").text,
        TerminatedDate=exec_info.find("TerminatedDate").text,
        XML=ET.tostring(node, encoding="utf-8"),
    )
    return test


def create_event(session, node, test):
    """
    Create an event in the database according to the content of the node in the
    XML test log file.
    """
    # the content node
    content = node.find("Content")

    # the common node
    common = node.find("Common")

    # get the device
    device = get_or_create(
        session,
        Device,
        DeviceName=node.get("Device"),
    )

    # get packet type
    packet_type = get_or_create(
        session,
        PacketType,
        Type=node.get("EventType"),
        IsInput=False,  # don't know what to put
    )

    # the collection
    collection = get_or_create(
        session,
        ParserCollection,
        CollectionName=content.find("Collection").text,
    )

    # create the event
    event = Event(
        DateProduction="T".join(
            [
                common.find("EventDate").text,
                common.find("EventTime").text
            ],
        ),
        XML=ET.tostring(node, encoding="utf-8"),
        device=device,
        packet_type=packet_type,
        test=test,
        Category=content.find("Category").text,
        Name=content.find("Name").text,
        collection=collection,
    )
    return event


class FakeDatabaseROC(Command):
    """
    Command to generate a fake database with tests and corresponding data.
    """
    __command__ = "fake_database"
    __command_name__ = "fake_database"
    __parent__ = "guest"
    __parent_arguments__ = ["base"]
    __help__ = "To generate a fake database for the MEB and the ROC"


class PopulateMEB(Command):
    """
    Command to populate the fake database.
    """
    __command__ = "fake_populate"
    __command_name__ = "populate"
    __parent__ = "fake_database"
    __parent_arguments__ = ["base"]
    __help__ = "Populate fake tables in specified databases"

    def add_arguments(self, parser):
        # argument to read the path to the configuration file to load
        parser.add_argument(
            "-m",
            '--meb',
            help="Name of the MEB database",
            type=str,
        )

        # prefix for the name of databases created
        parser.add_argument(
            '--name',
            help="Name of the database that will be created",
            type=str,
            default="roc_meb_test_db",
        )

        # number of databases to create
        parser.add_argument(
            '--number',
            help="Number of databases to create for tests",
            type=int,
            default=3,
        )

    def __call__(self, args):
        # get the database from the arguments
        meb = Database.manager[args.meb]

        # hack the database name
        meb.parameters["database"] = args.name

        # check connected
        meb.connectDatabase()

        # check it is connected
        if not meb.connected:
            logger.error("{0} not connected".format(meb))
            return

        # names for meb data databases to populate and store their informations
        databases = [
            "{0}_data_{1}".format(args.name, x)
            for x in range(1, args.number + 1)
        ]

        # generate databases
        session = meb.scoped_session()
        try:
            generate_database_information(session, databases)
            session.commit()

            # create meb selector
            selector = MEBSelector(meb)
            current = selector.current()
            current.connectDatabase()
            meb_data_session = current.scoped_session

            # put the xml data into the database
            data_to_meb(meb_data_session, paths.from_data())

        except:
            print_exception()


class CreateMEB(Command):
    """
    Command to create the databases of the MEB.
    """
    __command__ = "fake_meb_create"
    __command_name__ = "create_meb"
    __parent__ = "fake_database"
    __parent_arguments__ = []
    __help__ = "Create the databases for the MEB database"

    def add_arguments(self, parser):
        # argument to read the path to the configuration file to load
        parser.add_argument(
            "-m",
            '--meb',
            help="Name of the MEB database",
            type=str,
        )

        # prefix for the name of databases created
        parser.add_argument(
            '--name',
            help="Name of the database that will be created",
            type=str,
            default="roc_meb_test_db",
        )

        # number of databases to create
        parser.add_argument(
            '--number',
            help="Number of databases to create for tests",
            type=int,
            default=3,
        )

    def __call__(self, args):
        # get the database from the arguments
        meb = Database.manager[args.meb]

        # force no database
        meb.parameters["database"] = ""

        # check database available
        if not meb.is_available_with_error():
            logger.error("{0} not connected".format(meb))
            return

        # create the databases of the meb
        create_meb_databases(meb, args.name, args.number)


# vim: set tw=79 :
