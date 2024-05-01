import mysql.connector

def test_database_connection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,  # Default MySQL port
            user='root',
            password='ForevaEva2',
            database='HealthcareDB',
        )
        print("Database connection is valid.")
        conn.close()
    except mysql.connector.Error as err:
        print("Error:", err)

# Test the database connection
test_database_connection()

