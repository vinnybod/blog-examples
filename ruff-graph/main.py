from src import lib_c
import requests

lib_c.foo()

requests.get("https://www.google.com").text

if __name__ == "__main__":
    print("Hello from ruff-graph!")
