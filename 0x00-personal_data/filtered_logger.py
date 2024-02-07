#!/usr/bin/env python3
""" module for message obfuscating """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ log message obfuscated """
    for i in fields:
        message = re.sub(f'{i}=.*?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message
