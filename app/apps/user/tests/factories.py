from polyfactory.factories.beanie_odm_factory import BeanieDocumentFactory

from app.apps.user.models import User


class UserFactory(BeanieDocumentFactory):
    __model__ = User
