# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError # Add import

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password, host, port, database, collection): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = username
        PASS = password
        HOST = host
        PORT = port
        DB = database
        COL = collection
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        """Insert a document into the collection"""
        # If data is not empty, attempt inset into DB; else display error
        if data is not None:
            try:
                self.collection.insert_one(data)  # data should be dictionary
                # Return “True” if successful insert
                return True
            except PyMongoError as e:
                print(f'An error occurred while inserting the document: {e}')
                # If insert was not successful, return false
                return False 
        else: 
            raise Exception("Nothing to save, because data parameter is empty")

    # Create method to implement the R in CRUD.
    # Ref: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/cursors/
    def read(self, query):
        """Read all document in the specified database and collection"""
        # If query is not empty attempt read, else display error
        if query is not None:
            # Return result in a list if the command is successful, else an empty list
            try:
                cursor = self.collection.find(query)
                all_results = list(cursor)
                return all_results
            except PyMongoError as e:
                print(f'An error occurred while finding the documents: {e}')
                return []
        else:
            raise Exception("Query parameter is empty")
            
    # Create method to implement the U in CRUD
    # Ref: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/update/
    def update(self, query, new_data):
        """Update a document in the collection with new information and return the count of modifed items"""
        # If no query is passed in, raise error
        if query is None:
            raise Exception('Query parameter is empty')
        # If query is passed and new_data is not empty, try to update specified documents
        if new_data is not None:
            try:
                # Check for mongo operator to prevent crash
                # Check if new_data is a dictionary and if the key begins with a $
                if isinstance(new_data, dict) and not any(k.startswith('$') for k in new_data.keys()):
                    update_data = {'$set' : new_data}
                else:
                    update_data = new_data
                # Update document(s)
                # Note: update_many works dynamically with single and several documents
                results = self.collection.update_many(query, update_data)
                # Return number of modified documents
                return results.modified_count
            except PyMongoError as e:
                print(f'An error occurred while updating the document: {e}')
                # Because no documents were modified, return zero
                return 0
        else:
            raise Exception('New data parameter is empty')
                               
    # Create method to implement the D in CRUD
    def delete(self, query):
        """Delete a document from the collection"""
        # If query is not empty, try to delete the document(s), else return error
        if query is not None:
            try:
                results = self.collection.delete_many(query)
                # Return number of deleted documents
                return results.deleted_count
            except PyMongoError as e:
                print(f'An error occurred while deleting the document: {e}')
                # Because no documents were modified, return zero
                return 0
        else:
            raise Exception("Query parameter is empty")