import os

class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


    def __str__(self):
        return 'User(id={})'.format(self.id)

user = os.getenv('USER_FYLE')
password = os.getenv('PASSWORD_FYLE')


users = [
    User(1, user, password),
]
