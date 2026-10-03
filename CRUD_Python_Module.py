"""
File: CRUD_Python_Module.py
Author: Michael Rodman
Date: October 2, 2026
Course: CS 499 Computer Science Capstone
Version: 2.0

Purpose:
Provide secure and reusable CRUD operations for the Grazioso Salvare
MongoDB animal collection. CS 499 enhancements add input validation,
database indexing, aggregation support, safer error handling, and
protection against accidental unrestricted update/delete operations.
"""

from urllib.parse import quote_plus

from pymongo import ASCENDING, MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter:
    """CRUD and aggregation operations for the MongoDB animal collection."""

    def __init__(
        self,
        username,
        password,
        host='localhost',
        port=27017,
        database='aac',
        collection='animals'
    ):
        """Initialize the MongoDB client using externally supplied credentials."""

        if not username or not password:
            raise ValueError(
                'MongoDB username and password must be supplied through secure configuration.'
            )

        safe_username = quote_plus(str(username))
        safe_password = quote_plus(str(password))

        connection_uri = (
            f'mongodb://{safe_username}:{safe_password}'
            f'@{host}:{int(port)}/?authSource=admin'
        )

        self.client = MongoClient(
            connection_uri,
            serverSelectionTimeoutMS=5000
        )

        self.database = self.client[database]
        self.collection = self.database[collection]

        self._create_indexes()

    def _create_indexes(self):
        """Create the compound index used by rescue-animal filtering queries."""

        try:
            self.collection.create_index(
                [
                    ('animal_type', ASCENDING),
                    ('breed', ASCENDING),
                    ('sex_upon_outcome', ASCENDING),
                    ('age_upon_outcome_in_weeks', ASCENDING)
                ],
                name='rescue_filter_idx'
            )
        except PyMongoError:
            print('Unable to create MongoDB indexes.')

    @staticmethod
    def _validate_query(query):
        """Return True when a MongoDB query is represented by a dictionary."""

        return isinstance(query, dict)

    def create(self, data):
        """Insert one animal document into MongoDB."""

        if not isinstance(data, dict) or not data:
            return False

        try:
            result = self.collection.insert_one(data)
            return result.inserted_id is not None
        except PyMongoError:
            print('Unable to create the requested animal record.')
            return False

    def read(self, query, projection=None):
        """Return animal documents matching the supplied MongoDB query."""

        if not self._validate_query(query):
            return []

        try:
            results = self.collection.find(query, projection)
            return list(results)
        except PyMongoError:
            print('Unable to retrieve animal records.')
            return []

    def aggregate(self, pipeline):
        """Run a MongoDB aggregation pipeline and return the results."""

        if (
            not isinstance(pipeline, list)
            or not all(isinstance(stage, dict) for stage in pipeline)
        ):
            return []

        try:
            return list(self.collection.aggregate(pipeline))
        except PyMongoError:
            print('Unable to aggregate animal records.')
            return []

    def update(self, query, update_data):
        """
        Update animal documents matching the query.

        Empty queries are rejected to reduce the risk of unintentionally
        modifying every document in the collection.
        """

        if (
            not self._validate_query(query)
            or not query
            or not isinstance(update_data, dict)
            or not update_data
        ):
            return 0

        try:
            result = self.collection.update_many(
                query,
                {'$set': update_data}
            )
            return result.modified_count
        except PyMongoError:
            print('Unable to update animal records.')
            return 0

    def delete(self, query):
        """
        Delete animal documents matching the query.

        Empty queries are rejected to reduce the risk of unintentionally
        deleting every document in the collection.
        """

        if not self._validate_query(query) or not query:
            return 0

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError:
            print('Unable to delete animal records.')
            return 0

    def close(self):
        """Close the MongoDB client connection."""

        self.client.close()
