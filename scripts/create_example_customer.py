import os

import click
import requests
from requests.models import Response

from script_setup import *
from src.models import AddressType

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

    customer_address: dict = {
        "line1": "471 1st Street Ct",
        "line2": None,
        "city": "Gotham",
        "state": "IL",
        "zipcode": "60603",
        "type": AddressType.DELIVERY,
    }

    response: Response = requests.post(
        url=os.environ["CREATE_CUSTOMER_URL"],
        json=new_customer,
        headers=headers,
    )

    print_request_response(response)

    if response.status_code == 201:
        response: Response = requests.post(
            url=f"{os.environ['CREATE_CUSTOMER_URL']}/{new_customer['username']}/address",
            json=customer_address,
            headers=headers,
        )

        print_request_response(response)


if __name__ == "__main__":
    main()
