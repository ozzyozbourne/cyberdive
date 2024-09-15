from neo4j import GraphDatabase


class Neo4jClient:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, node_label, properties):
        with self.driver.session() as session:
            session.execute_write(self._create_node, node_label, properties)

    @staticmethod
    def _create_node(tx, node_label, properties):
        query = f"CREATE (n:{node_label} {{name: $name}})"
        tx.run(query, name=properties["name"])


client = Neo4jClient(uri="bolt://localhost:7687", user="neo4j", password="ozzy1234@#$")
client.create_node("Person", {"name": "John Doe"})
client.close()
