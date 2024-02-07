#!/usr/bin/env python3
""" module for message obfuscating """
from typing import List
import re


def filter_datum(fields: List, redaction: str, message: str, separator: str):
    """ 
        log message obfuscated
        Args:
            fields: a list of strings representing all fields to obfuscate
            redaction: a string representing by what the field will be obfuscated
            message: a string representing the log line
            separator: a string representing by which character is separating all fields in the log line (message)
        Return - log message obfuscated
    """
    for i in fields:
        pattern = f'(?<={i}=).*?(?={separator})'
        message = re.sub(pattern, redaction, message)
    return message
