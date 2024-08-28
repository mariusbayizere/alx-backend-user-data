#!/usr/bin/env python3
"""
filtered_logger module provides a function to obfuscate log messages.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message with sensitive fields obfuscated.

    Args:
        fields (List[str]): A list of strings representing all fields
                            to obfuscate.
        redaction (str): The string to replace the field's value with.
        message (str): The log message containing data to be obfuscated.
        separator (str): The character separating fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]+',
                         f'{field}={redaction}', message)
    return message
