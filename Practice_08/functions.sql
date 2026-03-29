CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    WHERE first_name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_phonebook_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;