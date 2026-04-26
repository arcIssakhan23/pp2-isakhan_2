import psycopg2
from configparser import ConfigParser



def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        return {param[0]: param[1] for param in parser.items(section)}
    else:
        raise Exception(f"Section {section} not found in {filename}")



def get_connection():
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None



def create_tables():
    conn = get_connection()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER NOT NULL,
        level_reached INTEGER NOT NULL,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """)

    conn.commit()
    cur.close()
    conn.close()



def get_or_create_player(username):
    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    result = cur.fetchone()

    if result:
        cur.close()
        conn.close()
        return result[0]

    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
    conn.commit()
    player_id = cur.fetchone()[0]

    cur.close()
    conn.close()
    return player_id



def save_game(player_id, score, level):
    if player_id is None:
        return

    conn = get_connection()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
    INSERT INTO game_sessions(player_id, score, level_reached)
    VALUES (%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()
    cur.close()
    conn.close()


#Leaderboard
def get_top_scores():
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    cur.execute("""
    SELECT username, score, level_reached, played_at
    FROM game_sessions
    JOIN players ON players.id = game_sessions.player_id
    ORDER BY score DESC
    LIMIT 10
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()
    return data



def get_personal_best(player_id):
    if player_id is None:
        return 0

    conn = get_connection()
    if conn is None:
        return 0

    cur = conn.cursor()

    cur.execute("""
    SELECT MAX(score) FROM game_sessions
    WHERE player_id = %s
    """, (player_id,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result if result else 0