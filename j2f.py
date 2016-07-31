#!/usr/bin/python3
from firebase import firebase

URL = "https://govhack-e9396.firebaseio.com/"

class FirebaseInterface:
	def __init__(self, URL):
		self.firebase = firebase.FirebaseApplication(URL, None)

	def postData(self, data):
		result = self.firebase.post('/user', new_user, data)
		print(result)

def SentimentDatabase:
	def __init__(self):
		self.base = ""

def main():
	fb = FirebaseInterface(URL)
	users = fb.getUsers()
	for u in users:
		print(u)

if __name__ == '__main__':
    main()

