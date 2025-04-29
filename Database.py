import sqlite3
import os


class Database:
    def __init__(self, db_name="metrics.db"):
        """Initialize the database connection."""
        if not os.path.exists("./db"):
            os.makedirs("./db")
        self.db_name = "./db/" + db_name
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish a connection to the database."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def get_cursor(self):
        """Return the database cursor."""
        if not self.connection:
            self.connect()
        return self.cursor

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def initDb(self, table_name):
        """Initialize the database with a specific table."""
        self.cursor = self.get_cursor()
        if table_name == "GetDataGitHub":
            self.cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    BATCH_ID INTEGER,
                    REPO_START_DATE TEXT,
                    REPO_END_DATE TEXT,
                    STAR_COUNT INTEGER,
                    NUMBER_OF_REPOS INTEGER,
                    NUMBER_OF_REPOS_SAVED INTEGER,
                    ELAPSED_TIME REAL,
                    SUCCESS_RATE REAL,
                    IS_FOLDER_UPDATE_EVENT BOOLEAN
                )
                """
            )
        self.connection.commit()

    def getBatId(self, table_name):
        """Get the last batch ID from the database."""
        self.cursor = self.get_cursor()
        self.cursor.execute(f"SELECT MAX(BATCH_ID) FROM {table_name}")
        result = self.cursor.fetchone()
        if result[0] is None:
            return 1
        else:
            return result[0] + 1
