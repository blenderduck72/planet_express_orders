import os
import sys
from pprint import pprint

from requests.models import Response

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))


def print_request_response(response: Response) -> None:
    print(f"Status: {response.status_code}")
    print("Response:")
    print("-------")
    pprint(response.json())
