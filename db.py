import sqlite3

def create_connection(db_file):
    """
    Create a connection to the SQLite database specified by db_file.
    If the database does not exist, it will be created.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
    return conn


def create_tables(conn):
    """
    Create tables in the connected SQLite database.
    """
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            dish_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES User (id),
            FOREIGN KEY (dish_id) REFERENCES Dishes (id)
        );
    """)

    conn.commit()
    print("Tables created (if they did not already exist).")


def insert_sample_data(conn):
    """
    Insert some sample data into the tables for demonstration.
    """
    cursor = conn.cursor()

    user_data = [
        ("user1", "user1@example.com", "password1"),
        ("user2", "user2@example.com", "password2"),
        ("user3", "user3@example.com", "password3"),
    ]
    cursor.executemany("""
        INSERT INTO User (login, email, password)
        VALUES (?, ?, ?);
    """, user_data)
    
    admin_data = [
        ("admin1", "admin1@example.com", "adminpass1"),
        ("admin2", "admin2@example.com", "adminpass2"),
    ]
    cursor.executemany("""
        INSERT INTO Admin (login, email, password)
        VALUES (?, ?, ?);
    """, admin_data)

    dishes_data = [
        ("Pizza", "Delicious cheese pizza", 9.99),
        ("Pasta", "Homemade pasta with tomato sauce", 7.49),
        ("Salad", "Fresh garden salad with dressing", 5.00),
    ]
    cursor.executemany("""
        INSERT INTO Dishes (title, description, price)
        VALUES (?, ?, ?);
    """, dishes_data)

    orders_data = [
        (1, 1), 
        (2, 3), 
        (3, 2),  
    ]
    cursor.executemany("""
        INSERT INTO Orders (user_id, dish_id)
        VALUES (?, ?);
    """, orders_data)

    conn.commit()
    print("Sample data inserted.")


def main():
    database = "example.db"
    conn = create_connection(database)

    if conn:
        create_tables(conn)
        insert_sample_data(conn)
        
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User;")
        print("Users:", cursor.fetchall())

        cursor.execute("SELECT * FROM Admin;")
        print("Admins:", cursor.fetchall())

        cursor.execute("SELECT * FROM Dishes;")
        print("Dishes:", cursor.fetchall())

        cursor.execute("""
            SELECT Orders.id, User.login, Dishes.title
            FROM Orders
            JOIN User ON Orders.user_id = User.id
            JOIN Dishes ON Orders.dish_id = Dishes.id;
        """)
        print("Orders (with related user and dish):", cursor.fetchall())

        conn.close()


if __name__ == "__main__":
    main()
