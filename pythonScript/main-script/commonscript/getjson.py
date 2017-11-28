# Python 3.6
# This is a library

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import simplejson

def get_json_from_url(url):
    # Load first JSON to get the total elements number
    try:
        response_data = urlopen(url).read()
        json_data = simplejson.loads(response_data)
    # Check if data is valid json
    except simplejson.scanner.JSONDecodeError:
        print('No valid JSON!')
    # Check if the link is reachable
    except HTTPError as e:
        print(e.code)
        print(e.read)
    # Check if there is a connection reset by peer
    except SocketError as e:
        print("Socket Error")
        print(e)

    return json_data
