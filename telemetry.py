# import psutil
# import time
# import mysql.connector
# from mysql.connector import Error

# def create_connection():
#     """ Create a database connection to the MySQL database """
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             database='power',
#             user='root',
#             password='captain'
#         )
#         if connection.is_connected():
#             print("Successfully connected to the database")
#         return connection
#     except Error as e:
#         print(f"Error while connecting to MySQL: {e}")
#         return None

# def collect_cpu_power():
#     """ Simulate collecting CPU power consumption data """
#     # Replace with actual method to collect CPU power data
#     return 50.0  # in watts (example value)

# def collect_nic_power():
#     """ Simulate collecting NIC power consumption data """
#     # Replace with actual method to collect NIC power data
#     return 5.0  # in watts (example value)

# def calculate_energy_consumption(cpu_power, nic_power, interval):
#     """ Calculate energy consumption in kilowatt-hours (kWh) """
#     # Energy (kWh) = Power (W) * Time (h)
#     total_power = cpu_power + nic_power
#     energy_consumption = (total_power * interval) / 3600.0  # interval in seconds
#     return energy_consumption

# def insert_data(connection, timestamp, cpu_power, nic_power, energy_consumption):
#     """ Insert data into the telemetry table """
#     try:
#         cursor = connection.cursor()
#         cursor.execute('''INSERT INTO telemetry (timestamp, cpu_power, nic_power, energy_consumption)
#                           VALUES (%s, %s, %s, %s)''', (timestamp, cpu_power, nic_power, energy_consumption))
#         connection.commit()
#         print(f"Data inserted: {timestamp}, CPU Power: {cpu_power}W, NIC Power: {nic_power}W, Energy Consumption: {energy_consumption}kWh")
#     except Error as e:
#         print(f"Failed to insert data into MySQL table: {e}")

# def collect_and_insert_data(connection):
#     try:
#         while True:
#             timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
#             cpu_power = collect_cpu_power()
#             nic_power = collect_nic_power()
#             interval = 5  # Collect data every 5 seconds
#             energy_consumption = calculate_energy_consumption(cpu_power, nic_power, interval)
#             insert_data(connection, timestamp, cpu_power, nic_power, energy_consumption)
#             time.sleep(interval)  # Collect data every interval seconds
#     except KeyboardInterrupt:
#         print("Data collection stopped by user.")
#     finally:
#         if connection.is_connected():
#             connection.close()
#             print("MySQL connection is closed")

# if __name__ == "__main__":
#     db_connection = create_connection()
#     if db_connection:
#         collect_and_insert_data(db_connection)




import psutil
import time
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection to the MySQL database."""
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

def collect_cpu_power():
    """Collect CPU power consumption data based on CPU utilization."""
    cpu_usage = psutil.cpu_percent(interval=1)
    max_cpu_power = 100.0  # example maximum power consumption in watts
    cpu_power = (cpu_usage / 100) * max_cpu_power
    return cpu_power

def collect_nic_power():
    """Simulate collecting NIC power consumption data."""
    # Simulating NIC power consumption as psutil doesn't provide direct NIC power metrics
    return 5.0  # in watts (example value)

def calculate_energy_consumption(cpu_power, nic_power, interval):
    """Calculate energy consumption in kilowatt-hours (kWh)."""
    # Energy (kWh) = Power (W) * Time (h)
    total_power = cpu_power + nic_power
    energy_consumption = (total_power * interval) / 3600.0  # interval in seconds
    return energy_consumption

def insert_data(connection, timestamp, cpu_power, nic_power, energy_consumption):
    """Insert data into the telemetry table."""
    try:
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO telemetry (timestamp, cpu_power, nic_power, energy_consumption)
                          VALUES (%s, %s, %s, %s)''', (timestamp, cpu_power, nic_power, energy_consumption))
        connection.commit()
        print(f"Data inserted: {timestamp}, CPU Power: {cpu_power}W, NIC Power: {nic_power}W, Energy Consumption: {energy_consumption}kWh")
    except Error as e:
        print(f"Failed to insert data into MySQL table: {e}")

def collect_and_insert_data(connection):
    try:
        interval = 5  # Collect data every 5 seconds
        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            cpu_power = collect_cpu_power()
            nic_power = collect_nic_power()
            energy_consumption = calculate_energy_consumption(cpu_power, nic_power, interval)
            insert_data(connection, timestamp, cpu_power, nic_power, energy_consumption)
            time.sleep(interval)  # Collect data every interval seconds
    except KeyboardInterrupt:
        print("Data collection stopped by user.")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    db_connection = create_connection()
    if db_connection:
        collect_and_insert_data(db_connection)
