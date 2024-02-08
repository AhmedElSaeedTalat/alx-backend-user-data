#!/usr/bin/env python3
""" module for message obfuscating """
from typing import List
import logging
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ filter log message to be obfuscated """
    pattern = '|'.join(list(map(lambda i: f'(?<={i}=).*?(?={separator})', fields)))
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
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
