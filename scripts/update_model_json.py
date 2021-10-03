from typing import List
import click
import simplejson as json

from script_setup import *  # must be imported prior to src imports

from src.models.order import Order
from src.models.customer import Customer

@click.command()
def main():
    with open("data_models.json", "w") as file:
        models: List[dict] = [Customer.schema(), Order.schema()]
        json.dump(models, file, indent=4, sort_keys=False)


if __name__ == "__main__":
    main()
