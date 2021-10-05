import os

import click
import requests
from requests.models import Response

from script_setup import *


headers: dict = {
    "x-api-key": os.environ["X_API_KEY"],
    "Content-Type": "application/json",
}


@click.command()
@click.option("-id", "--delivery_address_id")
def main(delivery_address_id: str) -> None:
    new_order: dict = {
        "customer_email": "philipfry@planetexpress.com",
        "delivery_address_id": f"{delivery_address_id}",
    }

    response: Response = requests.post(
        url=os.environ["CREATE_ORDER_URL"],
        json=new_order,
        headers=headers,
    )

    print_request_response(response)


if __name__ == "__main__":
    main()
