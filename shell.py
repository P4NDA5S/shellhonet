import os
import logging
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil

logging.basicConfig(filename="honeypot.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s")

class PowerShellHoneypot:
    def __init__(self):
        self.env_vars = os.environ.copy()
        self.log_environment()
        self.run_honeypot()

    def log_environment(self):
        """Mencatat variabel environment saat pertama kali berjalan."""
        logging.info("Starting honeypot with environment variables: %s", self.env_vars)

    def capture_command(self, command):
        """Mencatat dan meniru perintah PowerShell."""
        logging.info("Command executed: %s", command)
        if command.lower() == "dir":
            return "Simulated Directory List\nC:\\Windows\nC:\\Users"
        elif command.lower() == "ipconfig":
            return "Simulated IP Configuration\nIP Address: 192.168.1.30"
        elif command.lower() == "get-process":
            return self.simulate_process_list()
        else:
            return f"Simulated Output for: {command}"

    def simulate_process_list(self):
        """Mensimulasikan daftar proses yang sedang berjalan."""
        processes = [(p.info['pid'], p.info['name']) for p in psutil.process_iter(['pid', 'name'])]
        result = "PID    Process Name\n"
        for pid, name in processes:
            result += f"{pid:<6} {name}\n"
        return result

    def run_honeypot(self):
        """Loop utama untuk menjalankan tiruan PowerShell."""
        print("PowerShell Honeypot Simulation\nType 'exit' to stop.")
        while True:
            try:
                command = input("PS C:\\> ")
                if command.lower() == "exit":
                    print("Exiting honeypot.")
                    break
                result = self.capture_command(command)
                print(result)
            except KeyboardInterrupt:
                print("\nHoneypot terminated.")
                break

class FileMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logging.info(f'File {event.src_path} has been modified.')

    def on_created(self, event):
        logging.info(f'File {event.src_path} has been created.')

    def on_deleted(self, event):
        logging.info(f'File {event.src_path} has been deleted.')

    def on_moved(self, event):
        logging.info(f'File {event.src_path} has been moved to {event.dest_path}.')


def start_file_monitoring(path='.'):
    """Memulai monitor file sistem."""
    event_handler = FileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    logging.info("Started monitoring file changes in: %s", path)
    return observer


if __name__ == "__main__":
    try:
        observer = start_file_monitoring(path='.')

        honeypot = PowerShellHoneypot()

    except KeyboardInterrupt:
        print("\nTerminating honeypot and file monitoring.")
    finally:
        observer.stop()
        observer.join()
        logging.info("Honeypot and file monitoring stopped.")
