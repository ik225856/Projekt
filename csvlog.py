import argparse
import time
import NetFT
import csv
import os

DEFAULT_IP_ADDRESS = '192.168.1.1'
BASE_CSV_DIR = r'C:\Users\Ivan\Desktop\data logging'

def initialize_sensor(ip_address):
    """Initialize the sensor with the given IP address."""
    sensor = NetFT.Sensor(ip_address)
    return sensor

def get_unique_csv_file_path(base_dir):
    """Generate a unique CSV file path with a timestamp."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(base_dir, f'output_{timestamp}.csv')

def process_sensor_data(sensor, nula):
    """Continuously process sensor data and write to CSV."""
    csv_file_path = get_unique_csv_file_path(BASE_CSV_DIR)
    print(f"Logging data to {csv_file_path}")

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Force (N)'])  # Write header if needed

        start_time = time.time()  # Start the timer for the logging session

        try:
            while True:
                sensor.getForce()  # Ensure the sensor is updated
                sensor_data = sensor.force()
                if len(sensor_data) > 2:  # Check if force data is valid
                    # Calculate the time elapsed since the start of logging
                    elapsed_time = time.time() - start_time
                    Z_sila = (nula - sensor_data[2]) / 1000000
                    writer.writerow([elapsed_time, Z_sila])
                    print(f"Data saved: {Z_sila}")
                    
                    # Flush the data to the file periodically
                    file.flush()
                else:
                    print("Error: Sensor data invalid, force array too short")

                time.sleep(0.01)  # 100 Hz frequency (0.01s per sample)

        except KeyboardInterrupt:
            print("Exiting due to user interrupt")
        finally:
            print("Cleaning up...")
            # Ensure that all data is flushed to the file
            file.flush()
            os.fsync(file.fileno())  # Ensure data is written to disk

def main():
    """Main function to parse arguments and start data processing."""
    parser = argparse.ArgumentParser(description="CSV Logging Script")
    parser.add_argument('-n', '--nula', type=float, required=True, help="Zero value for force calculation")
    args = parser.parse_args()

    # Use the default IP address
    sensor = initialize_sensor(DEFAULT_IP_ADDRESS)
    nula = args.nula

    try:
        process_sensor_data(sensor, nula)
    except KeyboardInterrupt:
        print("Exiting due to user interrupt")
    finally:
        print("Cleaning up...")

if __name__ == '__main__':
    main()
