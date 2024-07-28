import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import datetime

def create_connection():
    """ Create a database connection to the MySQL database """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='power',
            user='root',
            password='captain'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def fetch_data(connection):
    """ Fetch data from the telemetry table """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT timestamp, cpu_power, nic_power, energy_consumption FROM telemetry")
        rows = cursor.fetchall()
        # Print the fetched data for debugging
        print("Fetched data:")
        for row in rows:
            print(row)
        return rows
    except Error as e:
        print(f"Failed to fetch data from MySQL table: {e}")
        return []

def plot_data(rows):
    """ Plot the data using matplotlib """
    timestamps = [row[0] for row in rows]
    cpu_power = [row[1] for row in rows]
    nic_power = [row[2] for row in rows]
    energy_consumption = [row[3] for row in rows]

    plt.figure(figsize=(10, 5))

    # Plot CPU power consumption
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, cpu_power, label='CPU Power (W)')
    plt.xlabel('Time')
    plt.ylabel('CPU Power (W)')
    plt.legend()

    # Plot NIC power consumption
    plt.subplot(3, 1, 2)
    plt.plot(timestamps, nic_power, label='NIC Power (W)', color='orange')
    plt.xlabel('Time')
    plt.ylabel('NIC Power (W)')
    plt.legend()

    # Plot energy consumption
    plt.subplot(3, 1, 3)
    plt.plot(timestamps, energy_consumption, label='Energy Consumption (kWh)', color='green')
    plt.xlabel('Time')
    plt.ylabel('Energy Consumption (kWh)')
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    db_connection = create_connection()
    if db_connection:
        data_rows = fetch_data(db_connection)
        if data_rows:
            plot_data(data_rows)
        db_connection.close()
        print("MySQL connection is closed")
