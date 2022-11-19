from schemas import userSchema
import motor.motor_asyncio as motor
import configparser

class Database:
    @classmethod
    async def connect(cls):
        self = cls()
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.dblink = self.config.get('DB', 'link')
        self.dbname = self.config.get('DB', 'name')
        self.client = motor.AsyncIOMotorClient(self.dblink)
        self._database = self.client.get_database(self.dbname)
        self._collections = { collection_name: self._database.get_collection(collection_name) for collection_name in await self._database.list_collection_names() }

        self.Users = Users(self._collections['users'], userSchema)
        return self

class Users:
    def __init__(self, collection, schema):
        self.collection = collection
        self.schema = schema

    async def create(self, id):
        userData = await self.collection.find_one({"id": id})
        if userData:
            return userData
        userData = self.schema.copy()
        userData.update({"id": id})
        await self.collection.insert_one(userData)
        return userData

    async def find(self, id):
        return await self.create(id)

    async def set(self, id, data):
        await self.collection.update_one({"id": id}, {"$set": data})

    async def increase(self, id, data):
        await self.collection.update_one({"id": id}, {"$inc": data})