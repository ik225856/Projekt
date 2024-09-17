#!/usr/bin/env python

from __future__ import print_function
import NetFT
import argparse
import time
import socket
import struct
import subprocess
import threading

# Define server address and port
SERVER_HOST = '192.168.0.1'  # Replace with your server's host
SERVER_PORT = 2000  # Replace with your server's port

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f'Connected to server {SERVER_HOST}:{SERVER_PORT}')
    return client_socket

parser = argparse.ArgumentParser(description="Read data from ATI NetFT sensors.")
parser.add_argument('ip',
                    metavar='ip address',
                    type=str,
                    help="The IP address of the sensor")
parser.add_argument('-t', '--torque',
                    dest='torque',
                    action='store_true',
                    help="Show torque values")
parser.add_argument('-f', '--force',
                    dest='force',
                    action='store_true',
                    help="Show force values")
parser.add_argument('-s', '--samples',
                    dest='samples',
                    type=int,
                    default=False,
                    metavar='N',
                    help="The number of samples to print")
parser.add_argument('-m', '--mean',
                    dest='mean',
                    type=int,
                    nargs='?',
                    const=10,
                    default=False,
                    metavar='N',
                    help="Tare the sensor with N datapoints before showing data (default 10)")
parser.add_argument('-c', '--continuous',
                    dest='continuous',
                    action='store_true',
                    help="Print data continuously")
args = parser.parse_args()

args.force, args.torque = \
    args.force or not args.force and not args.torque, \
    args.torque or not args.force and not args.torque

sensor = NetFT.Sensor(args.ip)

if args.mean:
    sensor.tare(args.mean)

if args.force and args.torque:
    data = sensor.measurement
    get = sensor.getMeasurement
elif args.force:
    data = sensor.force
    get = sensor.getForce
else:
    data = sensor.torque
    get = sensor.getTorque

def get_plc_variable_status(client_socket):
    try:
        data = client_socket.recv(2)  # Expecting 2 bytes of data
        if data:
            if data == b'\x01\x00':  # 0100 in Hex or 1 in Int
                return True
            elif data == b'\x00\x00':  # 0000 in Hex or 0 in Int
                return False
    except Exception as e:
        print(f"Error receiving PLC status: {e}")
    return None

def send_data_to_plc(client_socket):
    global running
    try:
        while running:
            sensor.getForce()
            a = sensor.force()
            if len(a) > 2:  # Ensure valid force data
                Z_sila = (nula - a[2]) / 1000000  # Calculate the force in newtons
                message = struct.pack('>f', Z_sila)
                client_socket.sendall(message)
            time.sleep(0.04)  # Adjust to your needs, currently set to real-time
    except KeyboardInterrupt:
        print('Exiting send_data_to_plc thread')
    finally:
        client_socket.close()  # Close the socket when done

def manage_csv_logging(client_socket):
    global running
    logging_process = None
    try:
        while running:
            plc_status = get_plc_variable_status(client_socket)
            if plc_status is not None:
                if plc_status:
                    if logging_process is None:
                        logging_process = subprocess.Popen([
                            'python', 'csvlog.py',
                            '-n', str(nula)  # Pass the nula value
                        ])
                        print("Started logging to CSV")
                else:
                    if logging_process:
                        logging_process.terminate()  # Immediately terminate the logging process
                        logging_process.wait()  # Ensure the CSV script finishes writing
                        logging_process = None
                        print("Stopped logging to CSV")
            time.sleep(0.01)  # Check PLC status every 100ms
    except KeyboardInterrupt:
        print('Exiting manage_csv_logging thread')
        if logging_process:
            logging_process.terminate()
            logging_process.wait()  # Ensure the CSV script finishes writing

if __name__ == '__main__':
    running = True
    try:
        if args.samples:
            sensor.getMeasurements(args.samples)
            for i in range(args.samples):
                sensor.receive()
                print(data())
        elif args.continuous:
            sensor.startStreaming(False)
            sensor.getForce()
            a = sensor.force()
            if len(a) > 2:  # Check if force data is valid
                nula = a[2]  # Set the initial nula value
            else:
                print("Error: Sensor data invalid at start, force array too short")
                exit(1)

            client_socket = connect_to_server()  # Ensure client_socket is available

            plc_thread = threading.Thread(target=send_data_to_plc, args=(client_socket,))
            plc_thread.daemon = True
            plc_thread.start()

            manage_csv_logging(client_socket)
        else:
            print(get())

    except KeyboardInterrupt:
        print("\nReceived CTRL+C, shutting down...")
        running = False  # Signal threads to exit
    finally:
        # Allow some time for threads to close properly
        time.sleep(0.1)
