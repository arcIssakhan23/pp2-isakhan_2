# Querying data using the fetchall() method




import psycopg2
from config import load_config

def get_users():
    """ Retrieve data using fetchall """

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT u.user_id, u.first_name, u.last_name, p.phone
                    FROM users u
                    INNER JOIN phones p ON p.user_id = u.user_id
                    ORDER BY u.first_name
                """)

                rows = cur.fetchall()

                print("The number of records: ", cur.rowcount)

                for row in rows:
                    print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    get_users()