import sys 
import os
import yaml
import flask
from urllib.parse import urlparse

app = flask.Flask(__name__)


@app.route("/")
def index():
    version = flask.request.args.get("urllib_version")
    url = flask.request.args.get("url")
    return fetch_website(version, url)

        
CONFIG = {"API_KEY": "771df488714111d39138eb60df756e6b"}
class Person(object):
    def __init__(self, name):
        self.name = name


def print_nametag(format_string, person):
    print(format_string.format(person=person))


def fetch_website(urllib_version, url):
    # Import only allowlisted urllib versions without dynamic code execution
    version = str(urllib_version).strip()
    if version == "3":
        import urllib3 as urllib
    else:
        raise ValueError("Unsupported urllib_version. Allowed values: '3'.")

    # Validate and restrict user-provided URL to trusted destinations (SSRF protection)
    parsed = urlparse(str(url).strip())
    allowed_hosts = {"www.google.com"}
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Unsupported URL scheme.")
    if not parsed.hostname or parsed.hostname not in allowed_hosts:
        raise ValueError("URL host is not allowed.")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in URL are not allowed.")

    safe_path = parsed.path or "/"
    safe_url = f"{parsed.scheme}://{parsed.hostname}{safe_path}"

    # Fetch and print the requested URL
    try: 
        http = urllib.PoolManager()
        r = http.request('GET', safe_url)
    except:
        print('Exception')


def load_yaml(filename):
    stream = open(filename)
    deserialized_data = yaml.load(stream, Loader=yaml.Loader) #deserializing data
    return deserialized_data
    
def authenticate(password):
    # Assert that the password is correct
    assert password == "Iloveyou", "Invalid password!"
    print("Successfully authenticated!")

if __name__ == '__main__':
    print("Vulnerabilities:")
    print("1. Format string vulnerability: use string={person.__init__.__globals__[CONFIG][API_KEY]}")
    print("2. Code injection vulnerability: use string=;print('Own code executed') #")
    print("3. Yaml deserialization vulnerability: see file_solution.yaml for a solution")
    print("4. Use of assert statements vulnerability: run program with -O argument")
    choice  = input("Select vulnerability: ")
    if choice == "1": 
        new_person = Person("Vickie")  
        print_nametag(input("Please format your nametag: "), new_person)
    elif choice == "2":
        urlib_version = input("Choose version of urllib: ")
        fetch_website(urlib_version, url="https://www.google.com")
    elif choice == "3":
        load_yaml(input("File name: "))
        print("Executed -ls on current folder")
    elif choice == "4":
        password = input("Enter master password: ")
        authenticate(password)

