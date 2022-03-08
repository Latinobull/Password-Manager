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
                self.add_password(key, value)

    def load_pass_file(self, path):
        self.password_file = path

        with open(path, 'r') as file:
            for line in file:
                site, encrypted = line.split(':')
                self.passowrd_dict[site] = Fernet(
                    self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as file:
                encrypted = Fernet(self.key).encrypt(password.encode())
                file.write(f'{site}:{encrypted.decode()}\n')

    def get_password(self, site):
        return self.passowrd_dict[site]


def main():
    password = {
        "test_email": 'testPassword',
        'test_account': 'testaccountPassword'
    }
    pm = PasswordManager()


if __name__ == '__main__':
    main()
