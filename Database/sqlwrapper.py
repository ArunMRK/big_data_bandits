import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)

# Getting Data from Aurora RDBS AWS source
rds_db = os.getenv('RDS_DB_NAME')
rds_user = os.getenv('RDS_USER')
rds_password = os.getenv('RDS_PASSWORD')
rds_host = os.getenv('RDS_HOST')


def get_db_connection() -> psycopg2.extensions.connection:
    """ Create a connection for database postgres Aurora"""
    try:
        conn = psycopg2.connect(f"""
    dbname={rds_db}
    user={rds_user} 
    password={rds_password}
    host={rds_host}""")
        return conn
    except:
        print("Error connecting to database.")


def query_executer(conn: psycopg2.extensions.connection ,query: str, params: tuple = ()) -> list:
    """An executor function for executing sql statements"""
    if conn != None:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            conn.commit()
            try:
                returned_data = cur.fetchall()
                return returned_data
            except:
                print("No results to fetch")
    else:
        return "No connection"