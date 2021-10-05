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
def main() -> None:
    new_order: dict = {
        "customer_email": "philipfry@planetexpress.com",
        "delivery_address_id": "0de92e53c7902597d4eaccab41dfefbb845f3387",
    }

    response: Response = requests.post(
        url=os.environ["CREATE_ORDER_URL"],
        json=new_order,
        headers=headers,
    )

    print_request_response(response)


if __name__ == "__main__":
    main()
