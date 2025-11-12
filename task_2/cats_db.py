import sys
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError

CONNECTION_STRING = "mongodb://localhost:27017/"

DB_NAME = "cats_db"
COLLECTION_NAME = "cats"


def get_db_collection():
    """
    Establishes connection to MongoDB and returns the collection object.
    Handles connection errors and exits if connection fails.
    """
    try:
        mongo_client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        mongo_client.admin.command('ping')
        print("MongoDB connection successful")

        db = mongo_client[DB_NAME]
        db_collection = db[COLLECTION_NAME]
        return db_collection, mongo_client

    except (ConnectionFailure, ConfigurationError) as e:
        print(f"Error: Failed to connect to MongoDB at {CONNECTION_STRING}")
        print(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected connection error: {e}")
        sys.exit(1)


def create_cat(collection, name, age, features):
    """
    Creates a new cat document in the collection.
    This is a helper function to add initial data.
    """
    try:
        doc = {"name": name, "age": age, "features": features}
        result = collection.insert_one(doc)
        print(f"Successfully created cat '{name}' with id: {result.inserted_id}")
    except OperationFailure as e:
        print(f"Error creating cat '{name}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def read_all_cats(collection):
    """
    Reads and prints all documents from the collection.
    """
    print("\nReading all cats")
    try:
        all_cats = collection.find()
        count = 0
        for cat in all_cats:
            print(cat)
            count += 1
        if count == 0:
            print("No cats found in collection")
    except OperationFailure as e:
        print(f"Error reading all cats: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def read_cat_by_name(collection, name):
    """
    Finds and prints a single cat document by its name.
    """
    print(f"\nFinding cat: '{name}'")
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Cat with name '{name}' not found")
    except OperationFailure as e:
        print(f"Error finding cat '{name}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def update_cat_age(collection, name, new_age):
    """
    Updates the 'age' of a cat specified by its name.
    """
    print(f"\nUpdating age for '{name}' -> {new_age}")
    try:
        result = collection.update_one(
            {"name": name},
            {"$set": {"age": new_age}}
        )

        if result.matched_count > 0:
            if result.modified_count > 0:
                print(f"Successfully updated age for '{name}'")
            else:
                print(f"Cat '{name}' found, but age was already {new_age}")
        else:
            print(f"Cat '{name}' not found. Update failed")
    except OperationFailure as e:
        print(f"Error updating cat '{name}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def add_feature_to_cat(collection, name, new_feature):
    """
    Adds a new feature to a cat's 'features' list by name.
    Uses $addToSet to avoid adding duplicate features.
    """
    print(f"\nAdding feature '{new_feature}' to cat '{name}'")
    try:
        result = collection.update_one(
            {"name": name},
            {"$addToSet": {"features": new_feature}}
        )

        if result.matched_count > 0:
            if result.modified_count > 0:
                print(f"Successfully added feature '{new_feature}' to '{name}'")
            else:
                print(f"Cat '{name}' found, but feature '{new_feature}' already exists")
        else:
            print(f"Cat '{name}' not found. Update failed")
    except OperationFailure as e:
        print(f"Error updating cat '{name}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def delete_cat_by_name(collection, name):
    """
    Deletes a single cat document from the collection by its name.
    """
    print(f"\nDeleting cat by name: '{name}'")
    try:
        result = collection.delete_one({"name": name})

        if result.deleted_count > 0:
            print(f"Successfully deleted cat '{name}'")
        else:
            print(f"Cat '{name}' not found. Delete failed")
    except OperationFailure as e:
        print(f"Error deleting cat '{name}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def delete_all_cats(collection):
    """
    Deletes all documents from the collection.
    """
    print("\nDeleting ALL cats from collection")
    try:
        result = collection.delete_many({})
        print(f"Successfully deleted {result.deleted_count} cats")
    except OperationFailure as e:
        print(f"Error deleting all cats: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    collection, client = get_db_collection()

    # 0. Start with a clean collection
    delete_all_cats(collection)

    # 1. (C) Create
    print("\nCreating new cats")
    create_cat(collection, "barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat(collection, "murzik", 5, ["любить спати", "ловить мишей"])
    create_cat(collection, "pushok", 1, ["дуже пухнастий", "боїться пилососа"])

    # 2. (R) Read - All
    read_all_cats(collection)

    # 3. (R) Read - One
    read_cat_by_name(collection, "murzik")
    read_cat_by_name(collection, "sonia")  # Test: non-existent cat

    # 4. (U) Update - Age
    update_cat_age(collection, "barsik", 4)
    read_cat_by_name(collection, "barsik")  # Check

    # 5. (U) Update - Add Feature
    add_feature_to_cat(collection, "barsik", "любить сметану")
    add_feature_to_cat(collection, "barsik", "рудий")  # Test: adding duplicate
    read_cat_by_name(collection, "barsik")  # Check

    # 6. (D) Delete - One
    delete_cat_by_name(collection, "pushok")
    read_all_cats(collection)  # Check

    # 7. (D) Delete - All (Cleanup)
    delete_all_cats(collection)
    read_all_cats(collection)  # Check

    if client:
        client.close()
        print("\nDatabase connection closed")