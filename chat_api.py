import requests
from bs4 import BeautifulSoup


url = "http://127.0.0.1:5000/chat"


if __name__ == '__main__':
    while True:
        user_input = input("user: ")

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        data = {"input": user_input}

        response = requests.post(url, json=data).json()

        soup = BeautifulSoup(response["response"], 'html.parser')
        pretty_html = soup.prettify()

        print(pretty_html)