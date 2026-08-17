import sqlite3

DATABASE_PATH = "database/rentlocal.db"


def verify_database():
    connection = sqlite3.connect(DATABASE_PATH)

    tables = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    ).fetchall()

    print("RENTLOCAL database schema")
    print("=" * 40)

    for table in tables:
        table_name = table[0]

        print(f"\n[{table_name}]")

        columns = connection.execute(
            f"PRAGMA table_info({table_name})"
        ).fetchall()

        for column in columns:
            column_id, name, data_type, not_null, default, primary_key = column

            print(
                f"  - {name} | "
                f"{data_type} | "
                f"PK={primary_key} | "
                f"NOT NULL={not_null}"
            )

    connection.close()


if __name__ == "__main__":
    verify_database()