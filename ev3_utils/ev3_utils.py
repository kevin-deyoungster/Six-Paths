import pysftp
import paramiko

def send_map_and_run(host="192.168.0.1", username="robot", password="maker", map_file, navigator_file):
    # Connect to the EV3 over SSH
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(host, username, password)

    # Send map and navigator file 
    sftp = ssh.open_sftp()
    sftp.put(map_file)
    sftp.put(navigator_file)
    
    # Run the navigator file
    commandstring = f"python3 {navigator_file}"
    ssh.exec_command(commandstring)

send_map_and_run(navigator_file="movement.py", map_file="planning_map.py")
