#!/usr/bin/env python3
""" module for message obfuscating """
from typing import List
import re


def filter_datum(fields: List, redaction: str, message: str, separator: str):
    """ log message obfuscated """
    for i in fields:
        pattern = f'(?<={i}=).*?(?={separator})'
        message = re.sub(pattern, redaction, message)
    return message
