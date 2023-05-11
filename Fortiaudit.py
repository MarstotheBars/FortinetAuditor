import os
import paramiko
import socket
import getpass

# construct the path to the hosts file
hosts_file = os.path.join(os.path.expanduser(
    '~'), 'Desktop', 'PyScripts', 'hosts.txt')

# read in the list of hosts from hosts.txt
with open(hosts_file) as f:
    hosts = [line.strip() for line in f]

# prompt for username and password
username = input('Enter your username: ')
password = getpass.getpass('Enter your password: ')

# prompt for command to run
command = input('Enter the command to run: ')

# connect to each host and run the command
with open('output.txt', 'w') as outfile:
    for host in hosts:
        try:
            # create SSH client object
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # connect to host with a 5-second timeout
            client.connect(hostname=host, port=9999, username=username,
                           password=password, timeout=5)
            print(f'Connecting to {host}...')
            # run command
            stdin, stdout, stderr = client.exec_command(command)
            # read and write output to file
            output = stdout.read().decode()
            lines = output.splitlines()
            if len(lines) > 1:
                output = '\n'.join(lines[:-1])
            else:
                output = ''
            outfile.write(f'{host}:\n{output}\n')
            # close the SSH connection
            client.close()
        except paramiko.ssh_exception.AuthenticationException:
            print(f'Authentication failed for {host}.')
            continue
        except paramiko.ssh_exception.SSHException as e:
            print(f'Could not connect to {host}: {e}')
            continue
        except socket.timeout:
            print(f'Timeout when connecting to {host}.')
            continue
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print(f'Could not connect to {host}: {e}')
            continue
