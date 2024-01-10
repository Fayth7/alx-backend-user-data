#!/usr/bin/env python3
"""
Module for handling Personal Data
"""

import logging
import os
import mysql.connector
from mysql.connector import connect


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] user_data %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_db():
    """
    Function to get a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection:
    """
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Establish a connection to the database
    db = connect(user=db_username, password=db_password,
                 host=db_host, database=db_name)

    return db


def main():
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=["name", "email",
                                                    "phone", "ssn",
                                                    "password"]))
    logger.addHandler(handler)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    columns = [i[0] for i in cursor.description]

    for row in cursor:
        log_msg = "Filtered data:\n"
        for col, value in zip(columns, row):
            log_msg += f"{col}: {value}; "
        logger.info(log_msg)

    cursor.close()
    db.close()


if __name__ == "__main__":
    # Code to execute when the script is run directly
    main()
