from app.libs.beanie_odm_ext import transaction
from app.libs.beanie_odm_ext.session import auto_session
from manage import fast_api_cli


async def create_product(category_obj):
    pass
    # product_obj = Product(name="test product94", description="prooduct test3", price=0.1, category=category_obj)
    # print(await product_obj.manage_session())

    # await product_obj.save()
    # raise Exception("Shit happens")


from pymongo import monitoring


class CommandLogger(monitoring.CommandListener):
    def started(self, event):
        # If a session is being used, 'lsid' will be in the command
        if "lsid" in event.command:
            print(f"🚀 Command: {event.command_name} | Session ID: {event.command['lsid']}")
        else:
            print(f"👻 Command: {event.command_name} | NO SESSION ATTACHED")

    def succeeded(self, event):
        pass

    def failed(self, event):
        pass


# Register the listener
monitoring.register(CommandLogger())


# @auto_session(read_concern=ReadConcern("majority"))
# @transaction.atomic(read_concern=ReadConcern("majority"))
async def session_test():
    pass
    # print(read_client.read_preference)

    # category_obj = Category(name="test4", description="olololoo3")
    #
    # # client = MongoDB.get_client()
    #
    # # async with await read_client.start_session() as session:
    #
    # #     await category_obj.save(session=session)
    #
    # await category_obj.save()
    #
    # await create_product(category_obj=category_obj)
    #
    # product_obj = Product(name="test product4", description="prooduct test3", price=0.1, category=category_obj)
    #
    # await product_obj.save()
    #
    # product_obj = await product_obj.find_one({"name": "test product4"})


@fast_api_cli.command("show_all_users")
async def show_all_users():
    async with auto_session():
        async with transaction.atomic():
            await session_test()
    # # print(read_client.read_preference)
    # category_obj = Category(name="test4", description="olololoo3")
    #
    # # client = MongoDB.get_client()
    # # async with await read_client.start_session() as session:
    # #     await category_obj.save(session=session)
    # await category_obj.save()
    # await create_product(category_obj=category_obj)
    #
    # product_obj = Product(name="test product4", description="prooduct test3", price=0.1, category=category_obj)
    # await product_obj.save()
    # product_obj = await product_obj.find_one({"name": "test product4"})
