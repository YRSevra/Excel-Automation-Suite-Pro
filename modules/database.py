import sqlite3
from datetime import datetime


DATABASE = "database/history.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS upload_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            upload_time TEXT,

            dataset_type TEXT,

            rows_count INTEGER,

            columns_count INTEGER,

            missing_values INTEGER,

            duplicate_rows INTEGER

        )
        """
    )

    conn.commit()

    conn.close()


def save_upload(

    filename,

    dataset_type,

    rows,

    columns,

    missing,

    duplicates

):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT INTO upload_history(

            filename,

            upload_time,

            dataset_type,

            rows_count,

            columns_count,

            missing_values,

            duplicate_rows

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            filename,

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            dataset_type,

            rows,

            columns,

            missing,

            duplicates

        )

    )

    conn.commit()

    conn.close()


def load_history():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT *

        FROM upload_history

        ORDER BY id DESC

        """

    )

    data = cursor.fetchall()

    conn.close()

    return data