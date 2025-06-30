from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class AnimalShelter:
    def __init__(self, username, password):
        try:
            self.client = MongoClient(
                f"mongodb://{username}:{password}@nv-desktop-services.apporto.com:33147",
                serverSelectionTimeoutMS=5000
            )
            self.database = self.client["AAC"]
        except ConnectionFailure as e:
            raise Exception(f"Failed to connect to MongoDB: {e}")
            
    def create(self, animal_data):
        if animal_data:
            result = self.database.animals.insert_one(animal_data)
            return result.acknowledged
        else:
            raise ValueError("No data provided to insert.")
    def read(self, query=None):
        if query:
            return list(self.database.animals.find(query, {"_id": False}))
        else:
            return list(self.database.animals.find({}, {"_id": False}))
        
    def update(self, filter_data, new_values):
        if filter_data and new_values:
            result = self.database.animals.update_many(filter_data, {"$set": new_values})
            return result.modified_count
        else:
            raise ValueError("Filter and new values must be provided.")
    def delete(self, query):
        if query:
            result = self.database.animals.delete_many(query)
            return result.deleted_count
        else:
            raise ValueError("Query needs to be provided in order to delete documents.")