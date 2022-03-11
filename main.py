from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

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
                self.password_dict[site] = Fernet(
                    self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as file:
                encrypted = Fernet(self.key).encrypt(password.encode())
                file.write(f'{site}:{encrypted.decode()}\n')

    def get_password(self, site):
        return self.password_dict[site]


def main():
    password = {
        "test_email": 'testPassword',
        'test_account': 'testaccountPassword'
    }
    pm = PasswordManager()

    print("""Choose an Option
    1) Create a new key
    2) Load an existing key
    3) Create a new password file
    4) Load existing password file
    5) Add a new password
    6) Get a password
    q) Quit application""")

    done = False

    while not done:
        choice = input("Pick an Option: ")
        if choice == '1':
            path = input('Name the file: ')
            pm.create_key(path)
        elif choice == '2':
            path = input('Enter file name: ')
            pm.load_key(path)
        elif choice == '3':
            path = input('Enter File name: ')
            pm.create_pass_file(path, password)
        elif choice == '4':
            path = input('Enter file name: ')
            pm.load_pass_file(path)
        elif choice == '5':
            site = input('Enter the site: ')
            password = input('Enter password: ')
            pm.add_password(site, password)
        elif choice == '6':
            site = input('Which site do you want to see: ')
            print(f'Password for {site} is {pm.get_password(site)} ')
        elif choice == 'q':
            done = True
            print('Have a great day!')
        else:
            print('Enter a valid choice please')


if __name__ == '__main__':
    main()
