#! /usr/bin/env python3

import os

from senzing import SzAbstractFactory, SzError
from senzing_core import SzAbstractFactoryCore

INSTANCE_NAME = "test"

RECORDS = {
    "1001": {
        "DataSource": "CUSTOMERS",
        "ID": "1001",
        "JSON": '{"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1001", "RECORD_TYPE": "PERSON", "PRIMARY_NAME_LAST": "Smith", "PRIMARY_NAME_FIRST": "Robert", "DATE_OF_BIRTH": "12/11/1978", "ADDR_TYPE": "MAILING", "ADDR_LINE1": "123 Main Street, Las Vegas NV 89132", "PHONE_TYPE": "HOME", "PHONE_NUMBER": "702-919-1300", "EMAIL_ADDRESS": "bsmith@work.com", "DATE": "1/2/18", "STATUS": "Active", "AMOUNT": "100"}',
    },
    "1002": {
        "DataSource": "CUSTOMERS",
        "ID": "1002",
        "JSON": '{"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1002", "RECORD_TYPE": "PERSON", "PRIMARY_NAME_LAST": "Smith", "PRIMARY_NAME_FIRST": "Bob", "DATE_OF_BIRTH": "11/12/1978", "ADDR_TYPE": "HOME", "ADDR_LINE1": "1515 Adela Lane", "ADDR_CITY": "Las Vegas", "ADDR_STATE": "NV", "ADDR_POSTAL_CODE": "89111", "PHONE_TYPE": "MOBILE", "PHONE_NUMBER": "702-919-1300", "DATE": "3/10/17", "STATUS": "Inactive", "AMOUNT": "200"}',
    },
    "1003": {
        "DataSource": "CUSTOMERS",
        "ID": "1003",
        "JSON": '{"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1003", "RECORD_TYPE": "PERSON", "PRIMARY_NAME_LAST": "Smith", "PRIMARY_NAME_FIRST": "Bob", "PRIMARY_NAME_MIDDLE": "J", "DATE_OF_BIRTH": "12/11/1978", "EMAIL_ADDRESS": "bsmith@work.com", "DATE": "4/9/16", "STATUS": "Inactive", "AMOUNT": "300"}',
    },
}


def add_datasources(sz_factory: SzAbstractFactory):
    sz_configmanager = sz_factory.create_configmanager()

    current_config_id = sz_configmanager.get_default_config_id()
    sz_config = sz_configmanager.create_config_from_config_id(current_config_id)

    for data_source in ("CUSTOMERS", "REFERENCE", "WATCHLIST"):
        sz_config.register_data_source(data_source)

    new_config = sz_config.export()
    new_config_id = sz_configmanager.register_config(
        new_config, "Code snippet register_data_source example"
    )
    sz_configmanager.replace_default_config_id(current_config_id, new_config_id)


def add_records(sz_factory: SzAbstractFactory):
    sz_engine = sz_factory.create_engine()
    for record in RECORDS.values():
        sz_engine.add_record(
            record.get("DataSource", ""), record.get("ID", ""), record.get("JSON", "")
        )


def count_redo_records(sz_factory: SzAbstractFactory):
    sz_engine = sz_factory.create_engine()
    result = sz_engine.count_redo_records()
    print(f"Redo record count: {result}")


def delete_records(sz_factory: SzAbstractFactory):
    sz_engine = sz_factory.create_engine()
    for record in RECORDS.values():
        sz_engine.delete_record(record.get("DataSource", ""), record.get("ID", ""))


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

try:

    # Create abstract factory.

    SETTINGS = os.getenv("SENZING_ENGINE_CONFIGURATION_JSON", "{}")
    sz_factory = SzAbstractFactoryCore(INSTANCE_NAME, SETTINGS, verbose_logging=False)

    # Add Data sources to Senzing repository.

    add_datasources(sz_factory)

    # Add, delete, count loop.

    for _ in range(10):
        add_records(sz_factory)
        delete_records(sz_factory)
        count_redo_records(sz_factory)


except SzError as err:
    print(f"\n{err.__class__.__name__} - {err}")
