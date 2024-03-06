import socket
import multiprocessing
import subprocess
import threading
import os
import time

minecraft_server_bat_path = "C:\\Users\\Jhon_Doee\\Documents\\minecraft_server\\run.bat"
working_directory = "C:\\Users\\Jhon_Doee\\Documents\\minecraft_server"
# replace with your ip
server_address = ("xxx.xxx.x.x", 25565)

server_running = False
socket_server_process = None  # Define the process globally
server_process = None  # Define the server process globally

def start_server():
    global server_running, server_process
    if not server_running:
        try:
            os.chdir(working_directory)        
            # Start the Minecraft server using subprocess to run the batch file
            server_process = subprocess.Popen([minecraft_server_bat_path])
            server_process.wait()  # Wait for the server process to finish
        except Exception as e:
            print(f"Error starting the server: {e}")
        finally:
            server_running = False

def is_server_running():
    try:
        with socket.create_connection((server_address), timeout=1):
            return True
    except (socket.error, socket.timeout):
        return False

def start_socket_server():
    global server_running, server_process

    print("Checking server status...")

    while True:
        if not server_running:
            # Check if the Minecraft server is online
            if is_server_running():
                print("Server is online.")
                time.sleep(10)  # Adjust the delay as needed
            else:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(server_address)
                    s.listen()

                    print("Server is offline. Checking for requests...")

                    conn, addr = s.accept()
                    print(f"Connection from {addr}")
                    conn.close()

                    # Start the Minecraft server in a separate thread
                    start_server_thread = threading.Thread(target=start_server)
                    start_server_thread.start()
                    server_running = True

def main():
    global socket_server_process
    # Start the socket server in a separate process
    socket_server_process = multiprocessing.Process(target=start_socket_server)
    socket_server_process.start()

if __name__ == "__main__":
    main()
