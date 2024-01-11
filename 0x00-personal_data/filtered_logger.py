#!/usr/bin/env python3

"""Function filter_datum that returns the log message obfuscated"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Return: the log message obfuscated
    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
    fields in the log line (message)
    """
    pattern = re.compile("|".join(
        [f"(?<={field}=)[^{separator}]*" for field in fields]))
    return pattern.sub(redaction, message)
