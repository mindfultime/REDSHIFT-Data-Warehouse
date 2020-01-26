from psycopg2 import Error
from sql_queries import create_table_queries, drop_table_queries, copy_table_queries, insert_table_queries


def table_actions(cur, conn, action):
    """
    The function is used to perform copy, create, insert, and drop tables in the connected database.
          :param cur: active cursor for connected database
          :param conn: connection to the database
          :param action: action to be performed in the connected database
    """
    try:
        table_queries = ""
        if action.lower() == 'drop':
            table_queries = drop_table_queries
        elif action.lower() == 'create':
            table_queries = create_table_queries
        elif action.lower() == 'insert':
            table_queries = insert_table_queries
        elif action.lower() == 'copy':
            table_queries = copy_table_queries
        else:
            print("Action is not selected, Please select \n "
                  "1. Drop to drop tables \n"
                  "2. Create to create tables \n"
                  "3. Insert to insert data into tables\n"
                  "4. Copy to copy data from S3 into tables")
        for query in table_queries:
            print(" {} Table \n Query: {}".format(action.title(), query))
            cur.execute(query)
            conn.commit()
            print("Completed !")
    except (Exception, Error) as e:
        print(e)


def main():
    print("Initiating Tables in Redshift")


if __name__ == "__main__":
    main()
