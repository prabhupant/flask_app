class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


    def __str__(self):
        return 'User(id={})'.format(self.id)

users = [
    User(1, 'fyle', 'bangalore'),
    User(2, 'google', 'mountainview')
]