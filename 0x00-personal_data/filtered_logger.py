#!/usr/bin/env python3

"""Function filter_datum that returns the log message obfuscated"""

import os
from typing import List, Tuple
import logging
import re
import mysql.connector

PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


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
    for field in fields:
        regex_pattern = fr'({field}=)[^{separator}]*({separator})'
        message = re.sub(regex_pattern, fr'\1{redaction}\2', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Method to filter values in incoming log records"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)

        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the database (mysql.connector.
    connection.MySQLConnection object
    """

    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root",
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or "",
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost",
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    Connection = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )

    return Connection


def main():
    """Main function"""
    db_connection = get_db()
    logger = get_logger()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        msg = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; "
            f"ssn={row[3]}; password={row[4]}; ip={row[5]}; "
            f"last_login={row[6]}; user_agent={row[7]};"
        )

        logger.info(msg)
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
