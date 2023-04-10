import requests
import json


class Codershq:
    API_URL = "https://assessment.codershq.ae"

    def __init__(self):
        self.token = ""
        self.r = requests.Session()

    def login(self, payload):
        base_url = "/api/rest-auth/login/"
        response = self.r.post(Codershq.API_URL + base_url, data=payload)
        print(response)
        data = json.loads(response.text)
        token = data["token"]
        self.r.headers["Authorization"] = f"Bearer {token}"
        return response

    def all_users(self):
        base_url = "/api/users/all/"
        url = Codershq.API_URL + base_url
        response = self.r.get(url)
        data = json.loads(response.text)
        return data

    def all_data(self):
        base_url = "/api/users/data/"
        url = Codershq.API_URL + base_url
        response = self.r.get(url)
        data = json.loads(response.text)
        return data
