import pysftp
import paramiko

# Defines the name of the file for download / upload


def send():
    remote_file = "planning_map.py"

    srv = pysftp.Connection(host="169.254.184.16", username="robot", password="maker")

    # Download the file from the remote server
    srv.put(remote_file)

    # Closes the connection
    srv.close()


def run():
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.connect("169.254.184.16", username="robot", password="maker")

    commandstring = "python3 planning_map.py"
    ssh.exec_command(commandstring)
    # readList = so.readlines()
    # errList = se.readlines()


send()
run()
