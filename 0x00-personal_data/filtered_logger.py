#!/usr/bin/env python3
""" module for message obfuscating """
from typing import List
import logging
import re
from mysql import connector
from os import environ


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ filter log message to be obfuscated """
    pattern = '|'.join(list(map(lambda i: f'(?<={i}=).*?(?={separator})',
                                fields)))
    return re.sub(pattern, redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ init function instantiantion"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format record as needed """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ creates logger """
    logger = logging.getLogger(name='user_data')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_db() -> connector.connection.MySQLConnection:
    """ return connector """
    user = environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    password = environ.get('PERSONAL_DATA_DB_PASSWORD', "")
    host = environ.get('PERSONAL_DATA_DB_HOST', "localhost")
    database = environ.get('PERSONAL_DATA_DB_NAME')
    connection = connector.connection.MySQLConnection(
            user=user,
            password=password,
            host=host,
            database=database)
    return connection
