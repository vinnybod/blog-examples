import src.lib_c as lib_c
import requests

lib_c.foo()

print(requests.get('https://www.google.com').text)

if __name__ == "__main__":
    print("Hello from ruff-graph!")
