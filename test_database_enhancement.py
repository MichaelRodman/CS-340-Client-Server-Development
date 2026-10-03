"""
File: test_database_enhancement.py
Author: Michael Rodman
Date: October 2, 2026
Course: CS 499 Computer Science Capstone

Purpose:
Verify the database-focused enhancements added to the Grazioso Salvare
AnimalShelter module without requiring a live MongoDB database.
"""

import unittest
from unittest.mock import MagicMock, patch

from CRUD_Python_Module import AnimalShelter


class TestDatabaseEnhancement(unittest.TestCase):

    def create_shelter(self):
        """Create an AnimalShelter instance with a mocked MongoDB connection."""

        with patch("CRUD_Python_Module.MongoClient") as mock_client:
            mock_database = MagicMock()
            mock_collection = MagicMock()

            mock_client.return_value.__getitem__.return_value = mock_database
            mock_database.__getitem__.return_value = mock_collection

            shelter = AnimalShelter(
                "test_user",
                "test_password"
            )

        return shelter, mock_collection

    def test_missing_credentials_are_rejected(self):
        """Credentials must be supplied through configuration."""

        with self.assertRaises(ValueError):
            AnimalShelter("", "")

    def test_rescue_filter_index_is_created(self):
        """The compound index should be created during initialization."""

        shelter, collection = self.create_shelter()

        collection.create_index.assert_called_once()

        args, kwargs = collection.create_index.call_args

        self.assertEqual(kwargs["name"], "rescue_filter_idx")
        self.assertEqual(
            [field for field, _ in args[0]],
            [
                "animal_type",
                "breed",
                "sex_upon_outcome",
                "age_upon_outcome_in_weeks"
            ]
        )

    def test_invalid_create_data_is_rejected(self):
        """Create should reject empty or non-dictionary data."""

        shelter, collection = self.create_shelter()

        self.assertFalse(shelter.create({}))
        self.assertFalse(shelter.create(None))

        collection.insert_one.assert_not_called()

    def test_invalid_read_query_returns_empty_list(self):
        """Read should reject a query that is not a dictionary."""

        shelter, collection = self.create_shelter()

        result = shelter.read("not-a-query")

        self.assertEqual(result, [])
        collection.find.assert_not_called()

    def test_aggregation_pipeline_is_sent_to_mongodb(self):
        """Aggregation should execute a valid MongoDB pipeline."""

        shelter, collection = self.create_shelter()

        pipeline = [
            {"$match": {"animal_type": "Dog"}},
            {"$group": {"_id": "$breed", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]

        collection.aggregate.return_value = [
            {"_id": "German Shepherd", "count": 4},
            {"_id": "Rottweiler", "count": 2}
        ]

        result = shelter.aggregate(pipeline)

        collection.aggregate.assert_called_once_with(pipeline)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["count"], 4)

    def test_invalid_aggregation_pipeline_is_rejected(self):
        """Aggregation should reject malformed pipeline input."""

        shelter, collection = self.create_shelter()

        self.assertEqual(shelter.aggregate("invalid"), [])
        self.assertEqual(shelter.aggregate([{"$match": {}}, "invalid"]), [])

        collection.aggregate.assert_not_called()

    def test_empty_update_query_is_rejected(self):
        """An empty query must not update the entire collection."""

        shelter, collection = self.create_shelter()

        result = shelter.update({}, {"breed": "Test Breed"})

        self.assertEqual(result, 0)
        collection.update_many.assert_not_called()

    def test_empty_delete_query_is_rejected(self):
        """An empty query must not delete the entire collection."""

        shelter, collection = self.create_shelter()

        result = shelter.delete({})

        self.assertEqual(result, 0)
        collection.delete_many.assert_not_called()


if __name__ == "__main__":
    unittest.main()
