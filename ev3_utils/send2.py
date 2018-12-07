import pysftp
import paramiko


def send():
    remote_file = "planning_map.py"
    srv = pysftp.Connection(host="192.168.0.1", username="robot", password="maker")
    srv.put(remote_file)
    srv.close()


def run():
    ssh = paramiko.SSHClient()  
    ssh.load_system_host_keys()
    ssh.connect("192.168.0.1", username="robot", password="maker")
    commandstring = "python3 movement.py"
    ssh.exec_command(commandstring)

def send_map_and_run(host="192.168.0.1", username="robot", password="maker", map_file_path, navigator_file_name):
    '''
    Refined function that combines both sending and receiving. Faster
    '''
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(host, username, password)
    sftp = ssh.open_sftp()
    sftp.put(map_file_path)
    commandstring = f"python3 {navigator_file_name}"
    ssh.exec_command(commandstring)



send()
run()
