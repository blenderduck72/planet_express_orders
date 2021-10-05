import os

import click
import requests
from requests.models import Response

from script_setup import *

url: str = os.environ["CREATE_ORDER_URL"]

headers: dict = {
    "x-api-key": os.environ["X_API_KEY"],
    "Content-Type": "application/json",
}


@click.command()
@click.option("-id", "--order_id")
def main(order_id: str) -> None:

    response: Response = requests.get(
        url=f"{os.environ['CREATE_ORDER_URL']}/{order_id}",
        headers=headers,
    )

    print_request_response(response)


if __name__ == "__main__":
    main()
