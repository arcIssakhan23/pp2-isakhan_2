import psycopg2
from config import load_config
import csv


def insert_user(first_name, last_name, phone):
    sql_user = """
        INSERT INTO users(first_name, last_name)
        VALUES(%s, %s) RETURNING user_id;
    """

    sql_phone = """
        INSERT INTO phones(user_id, phone)
        VALUES(%s, %s);
    """

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql_user, (first_name, last_name))
                user_id = cur.fetchone()[0]

                cur.execute(sql_phone, (user_id, phone))

            conn.commit()

    except Exception as error:
        print(error)


def insert_from_csv():
    try:
        with open("phone_book.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                insert_user(
                    row["first_name"],
                    row["last_name"],
                    row["phone"]
                )

        print("CSV data inserted!")

    except Exception as error:
        print(error)


def insert_from_console():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone = input("Phone: ")

    insert_user(first_name, last_name, phone)
    print("User added!")


if __name__ == "__main__":
    choice = input("Type 'csv' or 'console': ").lower()

    if choice == "csv":
        insert_from_csv()
    elif choice == "console":
        insert_from_console()
    else:
        print("Invalid input")