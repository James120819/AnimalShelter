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
        """
        Insert one document. Returns True if inserted, False otherwise. 
        Guards against bad input to avoid writing junk to the DB.
        """
        if not isinstance(animal_data, dict) or not animal_data:
            return False

        result = self.database.animals.insert_one(animal_data)
        return bool(result.inserted_id)
    
    def read(self, query=None, projection=None, limit=0, sort=None):
        """
        Consistent list:
        - query: dict of filters
        - projection: dict of fields to return; defaults to all except _id
        - limit: max number of docs (0 = no limit)
        - sort: list of (field, direction) pairs, [("age_upon_outcome_in_weeks", 1)]
        Returns: list of documents.
        """

       q = self._coerce_filter(query)
       proj = self._coerce_projection(projection)

       cursor = self.database.animals.find(q, proj)

       if sort:
           cursor = cursor.sort(sort)

       if limit:
           cursor = cursor.limit(int(limit))

        return list(cursor)
        
        
   
    def update(self, filter_data, new_values):
        """
        Update many documents matching filter_data with $set new_values.
        Returns the number of modified documents. 
        """
        if not isinstance(filter_data, dict) or not filter_data:
            return 0
        if not isinstance(new_values, dict) or not new_values:
            return 0

        result = self.database.animals.update_many(filter_data, {"$set": new_values})
        return result.modified_count
    
    def delete(self, query):
       """
       Delete many documents matching query.
       Returns the number of deleted documents.
       """
        if not isinstance(query, dict) or not query:
            return 0

        result = self.database.animals.delete_many(query)
        return result.deleted_count


     def _coerce_filter(self, query):
         """Return a dict Mongo can use, or {} if query is falsy/invalid."""
         return query if isinstance(query, dict) else {}

   
    def _coerce_projection(self, projection):
        """Default projection hides _id unless caller overrides."""
        return projection if isinstance(projection, dict) else {"_id": False}
