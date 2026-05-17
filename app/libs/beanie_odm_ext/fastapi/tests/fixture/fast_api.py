from contextlib import asynccontextmanager

from beanie import PydanticObjectId
from fastapi import FastAPI, APIRouter

from app.libs.beanie_odm_ext import transaction
from app.libs.beanie_odm_ext.fastapi.session_middleware import MongoSessionMiddleware
from app.libs.beanie_odm_ext.mongo_db import MongoDB
from app.libs.beanie_odm_ext.session import auto_session
from app.libs.beanie_odm_ext.tests.fixtures.models import Product, Category
from app.libs.managment.conf import settings
from app.utils.mongo_conf import transform_settings_to_mongo


@asynccontextmanager
async def lifespan_fixture(app: FastAPI):
    await MongoDB.init_beanie_db(
        db_name=settings.MONGO_DB_NAME,
        mongo_connection_params=transform_settings_to_mongo(settings),
        models_list=[Category, Product],
    )

    yield


router = APIRouter()


@router.post("/products")
@auto_session
@transaction.atomic
async def create_product():
    category = Category(name="Test category", description="test description")
    await category.save()
    product = Product(name="success_product", category=category, price=10)
    await product.save()
    return product


@router.post("/products_with_error")
@auto_session
@transaction.atomic
async def create_product_with_error():
    category = Category(name="Test category", description="test description")
    await category.save()
    product = Product(name="product_with_error", category=category, price=10)
    await product.save()

    raise Exception("Test error")


@router.get("/products/{product_id}")
@auto_session
async def get_product(product_id: PydanticObjectId):
    return await Product.find_one(Product.id == product_id)


@router.get("/excluded-products/{product_id}")
@auto_session
async def get_product(product_id: PydanticObjectId):
    return await Product.find_one(Product.id == product_id)


test_fast_api_app = FastAPI(lifespan=lifespan_fixture)
test_fast_api_app.add_middleware(MongoSessionMiddleware, atomic_requests=True)
test_fast_api_app.include_router(
    router,
)
