import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Description: Delete pre-existing tables to be able to create them from scratch
    Arguments:
        cur: the cursor object.
        conn: connection object to redshift.
    Returns:
        None
    """
    print("Droping tables")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Description: Create staging and dimensional tables declared on sql_queries script
    Arguments:
        cur: the cursor object.
        conn: connection object to redshift.
    Returns:
        None
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """ "
    Description:
        - Set up the database tables, create needed tables with the appropriate columns and constricts
        - Drops all the tables.
        - Creates all tables needed.
        - Closes the connection.
    Returns:
        None
    """
    config = configparser.ConfigParser()
    config.read("dwh.cfg")

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            *config["CLUSTER"].values()
        )
    )
    cur = conn.cursor()
    print("Connected to the cluster")

    drop_tables(cur, conn)
    create_tables(cur, conn)
    print("Created tables")

    conn.close()


if __name__ == "__main__":
    main()
