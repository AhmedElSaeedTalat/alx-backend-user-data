#!/usr/bin/env python3
""" module for message obfuscating """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ log message obfuscated """
    pattern = '|'.join(list(map(lambda i: f'(?<={i}=).*?(?={separator})', fields)))
    return re.sub(pattern, redaction, message)
