from pymongo import MongoClient


class AnimalShelter(object):
    """CRUD operations for the Animal collection in MongoDB."""

    def __init__(self, username, password, host='localhost', port=27017,
                 database='aac', collection='animals'):
        """Initialize the MongoDB client and connect to the requested collection.

        Parameters:
            username (str): MongoDB username.
            password (str): MongoDB password.
            host (str): MongoDB host address.
            port (int): MongoDB port number.
            database (str): Name of the MongoDB database.
            collection (str): Name of the MongoDB collection.
        """

        self.client = MongoClient(
            'mongodb://%s:%s@%s:%d/?authSource=admin' % (username, password, host, port)
        )
        
        self.database = self.client[database]
        self.collection = self.database[collection]

    def create(self, data):
        """Insert a document into the MongoDB collection.

        Parameters:
            data (dict): The document to insert.

        Returns:
            bool: True if the insert is successful, otherwise False.
        """

        if data is not None:
            try:
                self.collection.insert_one(data)
                return True
            except Exception as error:
                print("An error occurred while inserting the document:", error)
                return False
        else:
            return False

    def read(self, query):
        """Query documents from the MongoDB collection.

        Parameters:
            query (dict): The MongoDB query used to find documents.

        Returns:
            list: A list of matching documents, or an empty list if unsuccessful.
        """

        if query is not None:
            try:
                results = self.collection.find(query)
                return list(results)
            except Exception as error:
                print("An error occurred while reading documents:", error)
                return []
        else:
            return []

    def update(self, query, update_data):
        """Update document(s) in the MongoDB collection.

        Parameters:
            query (dict): The MongoDB query used to find documents to update.
            update_data (dict): The field/value pairs to update.

        Returns:
            int: The number of documents modified.
        """

        if query is not None and update_data is not None:
            try:
                result = self.collection.update_many(query, {"$set": update_data})
                return result.modified_count
            except Exception as error:
                print("An error occurred while updating documents:", error)
                return 0
        else:
            return 0

    def delete(self, query):
        """Delete document(s) from the MongoDB collection.

        Parameters:
            query (dict): The MongoDB query used to find documents to delete.

        Returns:
            int: The number of documents deleted.
        """

        if query is not None:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as error:
                print("An error occurred while deleting documents:", error)
                return 0
        else:
            return 0