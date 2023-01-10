import requests

class Account:
    def __init__(self, uid: int):
        self.uid = int(uid)
        data = requests.get(f"https://api.risticks.ru/user?id={self.uid}").json()
        self.username = data['username']
        self.likes = data['likes']
        self.dislikes = data['dislikes']
    def update(self):
        data = requests.get(f"https://api.risticks.ru/user?id={self.uid}").json()
        self.likes = data['likes']
        self.dislikes = data['dislikes']
        self.username = data['username']

class Stats:
    def __init__(self, users, pages):
        self.users = users
        self.pages = pages

def getstats():
    data = requests.get("https://api.risticks.ru/stats").json()
    return Stats(data['total_users'], data['total_pages'])

def search(name):
    return requests.get(f"https://api.risticks.ru/search?name={name}").json()

