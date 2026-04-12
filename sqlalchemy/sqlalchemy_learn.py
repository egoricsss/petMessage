from sqlalchemy import create_engine, text, Engine


def create_and_insert_data(engine, data):
    with engine.connect() as connection:
        connection.execute(
            text("CREATE TABLE IF NOT EXISTS USERS (id int, name str, age int)")
        )

        connection.execute(
            text("INSERT INTO users (id, name, age) VALUES (:id, :name, :age)"),
            data,
        )
        connection.commit()


def fetch_all_users(engine: Engine):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, age FROM users;"))
        result = [row for row in result.mappings()]
        return result


def fetch_users_by_age(engine: Engine, min_age: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, age FROM users WHERE age > :min_age"),
            {"min_age": min_age},
        )
        result = [row for row in result.mappings()]
        print(result)


def main():
    engine = create_engine(
        url="sqlite+pysqlite:///:memory:", pool_pre_ping=True, echo=True
    )
    data = [
        {"id": 1, "name": "Alice", "age": 23},
        {"id": 2, "name": "Bob", "age": 18},
        {"id": 3, "name": "Charlie", "age": 17},
        {"id": 4, "name": "Alex", "age": 20},
    ]
    create_and_insert_data(engine, data)

    fetch_users_by_age(engine, 18)


if __name__ == "__main__":
    main()
