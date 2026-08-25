import sqlite3

DATABASE = "../database/lab.db"


def get_connection():
    return sqlite3.connect(DATABASE)