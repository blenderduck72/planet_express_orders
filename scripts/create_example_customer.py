import os
from pprint import pprint

import requests
from requests.models import Response

import click

from script_setup import *

url: str = os.environ["CREATE_CUSTOMER_URL"]

headers: dict = {
    "x-api-key": os.environ["X_API_KEY"],
    "Content-Type": "application/json",
}


@click.command()
def main() -> None:
    new_customer: dict = {
        "email": "philipfry@planetexpress.com",
        "first_name": "philip",
        "last_name": "fry",
        "username": "pfry",
    }

    response: Response = requests.post(
        url=url,
        json=new_customer,
        headers=headers,
    )

    print(f"Status: {response.status_code}")
    print("Response:")
    print("-------")
    pprint(response.json())


if __name__ == "__main__":
    main()
