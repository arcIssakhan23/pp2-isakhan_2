CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_user(value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = value
       OR phone = value;
END;
$$;