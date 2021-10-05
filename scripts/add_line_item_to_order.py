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
@click.option("-id", "--order_id")
def main(order_id: str) -> None:
    new_line_item: dict = {
        "name": "Popplers",
        "description": "Omicronian enities of small proportions.",
        "quantity": 100,
    }

    response: Response = requests.post(
        url=f"{os.environ['CREATE_ORDER_URL']}/{order_id}/line_item",
        json=new_line_item,
        headers=headers,
    )

    print_request_response(response)


if __name__ == "__main__":
    main()
