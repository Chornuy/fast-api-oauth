import asyncclick as click
from bson import ObjectId

from app.libs.beanie_odm_ext import transaction
from app.libs.beanie_odm_ext.session import auto_session
from app.libs.beanie_odm_ext.tests.fixtures.click_async import fast_api_cli_test
from app.libs.beanie_odm_ext.tests.fixtures.models import Category, Product


@fast_api_cli_test.command()
@auto_session
@transaction.atomic
async def create_products():
    category = Category(name="Test category", description="test description")
    await category.save()
    product = Product(name="product_with_cli", category=category, price=10)
    await product.save()
    click.echo(f"{product.name}")


@fast_api_cli_test.command()
@auto_session
@transaction.atomic
async def create_products_with_error():
    click.echo("Creating products...")
    category = Category(name="Test category", description="test description")
    await category.save()
    product = Product(name="product_with_cli_error", category=category, price=10)
    await product.save()
    click.echo(f"{product.name}")
    raise Exception("Product creation failed")


@fast_api_cli_test.command()
@click.argument("product_id")
@auto_session
async def get_product(product_id: str):
    product = await Product.find_one(Product.id == ObjectId(product_id))
    click.echo(f"{str(product.id)}")
