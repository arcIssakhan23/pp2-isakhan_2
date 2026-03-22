def update_user_and_phone(user_id, first_name, last_name, phone):
    """ Update both user and phone """

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    UPDATE users
                    SET first_name = %s,
                        last_name = %s
                    WHERE user_id = %s
                """, (first_name, last_name, user_id))

                cur.execute("""
                    UPDATE phones
                    SET phone = %s
                    WHERE user_id = %s
                """, (phone, user_id))

            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)