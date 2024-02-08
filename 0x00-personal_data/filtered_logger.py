#!/usr/bin/env python3
""" module for message obfuscating """
from typing import List
import logging
import re
from mysql import connector
import os


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
    usr = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    ps = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    """ connect to db """
    connection = connector.connection.MySQLConnection(
            user=usr,
            password=ps,
            database=db,
            host=host
            )
    return connection
