from ..utils.config import logger

# from py2neo import Graph, Node, Relationship

# Connect to the local Neo4j instance
# graph = Graph("bolt://host.docker.internal:7687", auth=("neo4j", "test"))


# Create dummy data
def create_dummy_data():
    # Create article nodes
    article1 = Node(
        "Article", id="A1", title="Article 1", content="Content of article 1"
    )
    article2 = Node(
        "Article", id="A2", title="Article 2", content="Content of article 2"
    )

    # Create assertion nodes
    assertion1 = Node("Assertion", id="AS1", text="Assertion 1 in article 1")
    assertion2 = Node("Assertion", id="AS2", text="Assertion 2 in article 1")
    assertion3 = Node("Assertion", id="AS3", text="Assertion 1 in article 2")

    # Create relationships
    graph.create(Relationship(article1, "CONTAINS", assertion1))
    graph.create(Relationship(article1, "CONTAINS", assertion2))
    graph.create(Relationship(article2, "CONTAINS", assertion3))

    # Create paper nodes
    paper1 = Node("Paper", id="P1", title="Paper 1", abstract="Abstract of paper 1")
    paper2 = Node("Paper", id="P2", title="Paper 2", abstract="Abstract of paper 2")

    # Create relationships between papers and assertions
    graph.create(Relationship(paper1, "SUPPORTS", assertion1))
    graph.create(Relationship(paper2, "CONTRADICTS", assertion2))

    print("Dummy data created.")


# Read data
def read_data():
    query = """
    MATCH (a:Article)-[:CONTAINS]->(as:Assertion)
    OPTIONAL MATCH (as)<-[:SUPPORTS]-(p:Paper)
    RETURN a.title AS article, as.text AS assertion, collect(p.title) AS supporting_papers
    """
    results = graph.run(query)
    logger.info("query %s", query)
    logger.info("results %s", results)
    for record in results:
        print(
            f"Article: {record['article']}, Assertion: {record['assertion']}, Supporting Papers: {record['supporting_papers']}"
        )
    return results


# Update data
def update_data():
    query = """
    MATCH (a:Article {id: 'A1'})
    SET a.content = 'Updated content of article 1'
    RETURN a
    """
    graph.run(query)
    print("Article A1 content updated.")


# Delete data
def delete_data():
    query = """
    MATCH (a:Article {id: 'A2'})
    DETACH DELETE a
    """
    graph.run(query)
    print("Article A2 deleted.")


# if __name__ == "__main__":
#     # Uncomment the functions below to test each operation

#     # Create dummy data
#     create_dummy_data()

#     # Read data
#     read_data()

#     # Update data
#     update_data()

#     # Read data again to verify update
#     read_data()

#     # Delete data
#     delete_data()

#     # Read data again to verify deletion
#     read_data()
