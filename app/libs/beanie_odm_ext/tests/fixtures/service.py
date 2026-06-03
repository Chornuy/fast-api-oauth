from pymongo.read_concern import ReadConcern

from app.libs.beanie_odm_ext import session, transaction
from app.libs.beanie_odm_ext.session import auto_session
from app.libs.beanie_odm_ext.tests.fixtures.models import Category, Product


@auto_session
@transaction.atomic
async def create_product():
    category = Category(name="Test category", description="test description")
    await category.save()
    product = Product(name="product_with_service", category=category, price=10)
    await product.save()
    return product


@auto_session
@transaction.atomic
async def create_product_with_error():
    category = Category(name="Test category", description="test description")
    await category.save()
    product = Product(name="product_with_service_with_error", category=category, price=10)
    await product.save()
    raise Exception("Product creation failed")


@auto_session(causal_consistency=True)
@transaction.atomic(read_concern=ReadConcern("majority"))
async def create_product_with_params():
    category = Category(name="Test category", description="test description")
    await category.save()
    product = Product(name="product_with_service_with_error", category=category, price=10)
    await product.save()


@auto_session
async def get_product(product_id: str):
    return await Product.find_one(Product.id == product_id)


async def create_product_using_context():
    async with session.auto_session():
        async with transaction.atomic():
            category = Category(name="Test category", description="test description")
            await category.save()
            product = Product(name="product_with_service_context", category=category, price=10)
            await product.save()


async def create_product_using_context_error():
    async with session.auto_session():
        async with transaction.atomic():
            category = Category(name="Test category", description="test description")
            await category.save()
            product = Product(name="product_with_service_context", category=category, price=10)
            await product.save()
            raise Exception("Product creation failed")


async def create_product_with_params_context():
    async with session.auto_session(causal_consistency=True):
        async with transaction.atomic(read_concern=ReadConcern("majority")):
            category = Category(name="Test category", description="test description")
            await category.save()
            product = Product(name="product_with_service_context", category=category, price=10)
            await product.save()
