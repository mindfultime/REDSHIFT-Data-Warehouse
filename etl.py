import configparser
import psycopg2
import database


def main():
    # getting configuration for aws
    config = configparser.ConfigParser()
    config.read('aws.cfg')

    # connecting to redshift cluster
    print(*config['CLUSTER'].values())
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    # Dropping Tables in Redshift
    database.table_actions(cur, conn, 'drop')

    # Creating Tables in Redshift
    database.table_actions(cur, conn, 'create')

    # Copying S3 bucket to staging tables
    database.table_actions(cur, conn, 'copy')

    # Inserting data from staging tables to star schema
    database.table_actions(cur, conn, 'insert')

    # closing connection
    conn.close()


if __name__ == "__main__":
    main()
