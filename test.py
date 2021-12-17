from json import dumps
from requests import post


response = post('http://127.0.0.1:5000/transform',
                data=dumps({'word': 'елка'}),
                headers={'content-type': 'application-json'})
print(response.json())