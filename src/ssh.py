from sshtunnel import SSHTunnelForwarder
from config import Settings

settings = Settings()

ssh_host = settings.SSH_HOST
ssh_port = settings.SSH_PORT
ssh_username = settings.SSH_USERNAME
ssh_key_filename = settings.SSH_KEYFILE

db_host = settings.DB_HOST
db_port = settings.DB_PORT

local_host = 'localhost'
local_port = 3307


class SSHConnection:
    def __init__(self):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_username = ssh_username
        self.ssh_key_filename = ssh_key_filename
        self.remote_bind_address = (db_host, db_port)
        self.local_bind_address = (local_host, local_port)
        self.ssh_client = None

    def check_ssh_key_permission(self):
        try:
            with open(self.ssh_key_filename, 'r'):
                print(f"You have permission to read the key file: {self.ssh_key_filename}")
        except PermissionError:
            print(f"You do not have permission to read the key file: {self.ssh_key_filename}")
            exit(1)

    def connect(self):
        print(f"Connecting to SSH host: {self.ssh_host}:{self.ssh_port} with username: {self.ssh_username}")
        try:
            self.check_ssh_key_permission()
            self.ssh_client = SSHTunnelForwarder(
                self.ssh_host,
                self.ssh_port,
                ssh_username=self.ssh_username,
                ssh_pkey=self.ssh_key_filename,
                remote_bind_address=self.remote_bind_address,
                local_bind_address=self.local_bind_address,
            )
        except Exception as e:
            print(f"Error connecting to SSH: {e}")
            exit(1)
        else:
            print("SSH connection successful.")
            self.ssh_client.start()

    def close(self):
        print(f'Closing SSH connection : {self.ssh_host}:{self.ssh_port} with username: {self.ssh_username}')
        if self.ssh_client:
            self.ssh_client.stop()


def get_ssh_connection():
    ssh_connection = SSHConnection()
    ssh_connection.connect()
    return ssh_connection
