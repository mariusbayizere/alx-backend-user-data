#!/usr/bin/env python3
"""
filtered_logger module provides a function to obfuscate log messages
and a logging formatter class to handle sensitive data.
"""

import re
import logging
from typing import List, Tuple


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class to handle sensitive information in logs. """

    REDACTION = "****"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter with fields to be obfuscated.

        Args:
            fields (List[str]): List of fields to be obfuscated in logs.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using `filter_datum`.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record with sensitive fields obfuscated.
        """
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log_message,
                            self.SEPARATOR)


# Define the PII_FIELDS tuple
PII_FIELDS: Tuple[str, ...] = ("name", "email", "ssn", "password", "phone")


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named 'user_data' to handle sensitive logs.

    Returns:
        logging.Logger: Configured logger with RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
