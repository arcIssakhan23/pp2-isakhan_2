def delete_by_name(first_name):
    """ Delete users by first name """

    rows_deleted = 0
    sql = 'DELETE FROM users WHERE first_name = %s'
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name,))
                rows_deleted = cur.rowcount

            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        return rows_deleted