import os
from elasticsearch import Elasticsearch
from neo4j import GraphDatabase

class Database:
    def __init__(self):
        self.es_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
        
        self.es = None
        self.neo4j_driver = None

    def connect(self):
        # Connect to Elasticsearch
        try:
            self.es = Elasticsearch([self.es_url])
            if self.es.ping():
                print("Connected to Elasticsearch")
            else:
                print("Could not connect to Elasticsearch")
        except Exception as e:
            print(f"Error connecting to Elasticsearch: {e}")

        # Connect to Neo4j
        try:
            self.neo4j_driver = GraphDatabase.driver(
                self.neo4j_uri, 
                auth=(self.neo4j_user, self.neo4j_password)
            )
            self.neo4j_driver.verify_connectivity()
            print("Connected to Neo4j")
        except Exception as e:
            print(f"Error connecting to Neo4j: {e}")

    def close(self):
        if self.neo4j_driver:
            self.neo4j_driver.close()

db = Database()
