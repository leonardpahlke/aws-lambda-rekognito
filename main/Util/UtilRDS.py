import sys
import pymysql
import logging
from Util.Util import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CREATE_TABLE_QUERY = "create table Celebrities ( " \
                     "CelebID  int NOT NULL, " \
                     "Name varchar(255) NOT NULL, " \
                     "S3ImageKey varchar(255) NOT NULL, " \
                     "Confidence float NOT NULL, " \
                     "PRIMARY KEY (CelebID))"


class RDSDatabase:
    def __init__(self, config: RDSConfig = RDSConfig()):
        self.db_name = config.db_name
        self.host = config.db_host
        self.port = config.db_port
        self.username = config.db_user
        self.password = config.db_password
        self.conn = None

    # Connect to MySQL Database
    def open_connection(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(self.host,
                                            user=self.username,
                                            passwd=self.password,
                                            db=self.db_name,
                                            connect_timeout=5)
        except pymysql.MySQLError as e:
            logging.error(e)
            sys.exit()
        finally:
            logging.info('Connection opened successfully.')

    # close connection to database
    def close_connection(self):
        self.conn.close()
        self.conn = None
        print('Database connection closed.')

    # Execute SQL query.
    def run_query(self, query):
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                records = [row for row in result]
                cur.close()
                return records
        except pymysql.MySQLError as e:
            print(e)
        finally:
            if self.conn:
                self.close_connection()


RDSDatabase().run_query(CREATE_TABLE_QUERY)
