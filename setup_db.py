import oracledb

WALLET_DIRECTORY = r"/opt/oracle"
DB_USER = "admin"
DB_PASSWORD = "Pa$$w0rd5678"
DB_DSN = "glxs3dqea9h0rmo0_high"

DDL = [
    """CREATE TABLE meal_options (
        id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name        VARCHAR2(200) NOT NULL,
        week_start  DATE NOT NULL,
        week_end    DATE NOT NULL
    )""",
    """CREATE TABLE meal_ratings (
        id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        option_id   NUMBER NOT NULL REFERENCES meal_options(id),
        score       NUMBER(4,1) NOT NULL,
        rated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""
]

# Semana actual: 27 Abril - 3 Mayo 2026
WEEK_START = "2026-04-27"
WEEK_END   = "2026-05-03"

INITIAL_OPTIONS = [
    "Hamburguesa, papas caseras y sopa de codito",
    "Tacos del Chava",
    "Desayuno McDonald's",
    "Pizzita de la Sierra",
    "Botanita",
    "Fruta",
]

def setup():
    print("Connecting to Oracle...")
    with oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN,
        config_dir=WALLET_DIRECTORY,
        wallet_location=WALLET_DIRECTORY,
        wallet_password=DB_PASSWORD
    ) as conn:
        print("Connected.")
        with conn.cursor() as cur:

            # Create tables
            for ddl in DDL:
                table_name = ddl.split("TABLE")[1].split("(")[0].strip()
                try:
                    cur.execute(ddl)
                    print(f"Table {table_name} created.")
                except oracledb.DatabaseError as e:
                    if "ORA-00955" in str(e):
                        print(f"Table {table_name} already exists, skipping.")
                    else:
                        raise

            # Insert initial options
            for name in INITIAL_OPTIONS:
                cur.execute(
                    """INSERT INTO meal_options (name, week_start, week_end)
                       VALUES (:name,
                               TO_DATE(:week_start, 'YYYY-MM-DD'),
                               TO_DATE(:week_end,   'YYYY-MM-DD'))""",
                    {"name": name, "week_start": WEEK_START, "week_end": WEEK_END}
                )
                print(f"Inserted: {name}")

            conn.commit()
            print("\nSetup complete.")

if __name__ == "__main__":
    setup()
