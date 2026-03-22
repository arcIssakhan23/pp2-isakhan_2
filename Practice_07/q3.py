# Querying data using the fetchmany() method



import psycopg2
from config import load_config


def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row


def get_user_phones():
    """ Retrieve joined data with iterator """

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT u.first_name, u.last_name, p.phone
                    FROM users u
                    INNER JOIN phones p ON p.user_id = u.user_id
                    ORDER BY u.first_name
                """)

                for row in iter_row(cur, 10):
                    print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    get_user_phones()