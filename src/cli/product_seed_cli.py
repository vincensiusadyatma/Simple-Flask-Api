import click
from flask.cli import with_appcontext
from ..seeders.product_seed import productSeed

@click.command("seed")
@with_appcontext
def product_seed():
    productSeed()
