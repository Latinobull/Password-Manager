from mimetypes import init
from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.passowrd_dict = None

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as file:
            file.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as file:
            self.key = file.read()

    def create_pass_file(self, path, initial=None):
        self.password_file = path

        if initial is not None:
            for key, value in initial.items():
                pass  # TODO PASSWORD FUNCTION

    def load_pass_file(self, path):
        self.password_file = path

        with open(path, 'r') as file:
            for line in file:
                site, encrypted = line.split(':')
                self.passowrd_dict[site] = Fernet(
                    self.key).decrypt(encrypted.encode()).decode()
