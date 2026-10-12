import os

from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
load_dotenv()

def get_neo4j_conn():
    return Neo4jGraph(
        url=os.getenv("NEO4J_URL"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        database=os.getenv("NEO4J_DATABASE", "neo4j")
    )


if __name__ == '__main__':
    print(get_neo4j_conn())