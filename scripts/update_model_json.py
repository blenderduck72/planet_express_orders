import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import click
import simplejson as json
from src.models.order import Order
from src.models.customer import Customer


@click.command()
def main():
    with open("data_models.json", "w") as file:
        models: List[dict] = [Customer.schema(), Order.schema()]
        json.dump(models, file, indent=4, sort_keys=False)


if __name__ == "__main__":
    main()
