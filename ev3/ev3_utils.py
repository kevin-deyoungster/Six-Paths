"""
This module contains SSH methods on the EV3
"""

import os
import paramiko
import stat


def send_map_and_run(
    map_file, navigator_file, host, username="robot", password="maker"
):
    """
    Sends map file to EV3 and runs the navigator which uses that file
    """

    # Make Navigator Executable
    st = os.stat(navigator_file)
    os.chmod(navigator_file, st.st_mode | stat.S_IEXEC)

    # Connect to the EV3 over SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, username=username, password=password)

    # Send map and navigator file to EV3
    sftp = ssh.open_sftp()
    sftp.put(map_file, map_file)
    sftp.put(navigator_file, navigator_file)
    print("Map and Navigator sent to EV3")

    # Run the navigator file
    commandstring = f"python3 {navigator_file}"
    ssh.exec_command(commandstring)
    print(f"Running Navigator {navigator_file}")


send_map_and_run(
    host="169.254.210.172", navigator_file="navigator.py", map_file="planning_map.py"
)
