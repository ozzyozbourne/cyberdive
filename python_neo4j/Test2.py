import re
from pydantic import BaseModel, Field
from typing import Optional
from neo4j import GraphDatabase


# Define the DocMeta Pydantic model
class DocMeta(BaseModel):
    BrowsingSessionId: Optional[str] = Field(default=None, description="BrowsingSessionId of Document")
    VisitedWebPageURL: Optional[str] = Field(default=None, description="VisitedWebPageURL of Document")
    VisitedWebPageTitle: Optional[str] = Field(default=None, description="VisitedWebPageTitle of Document")
    VisitedWebPageDateWithTimeInISOString: Optional[str] = Field(default=None,
                                                                 description="VisitedWebPageDateWithTimeInISOString of Document")
    VisitedWebPageReffererURL: Optional[str] = Field(default=None, description="VisitedWebPageReffererURL of Document")
    VisitedWebPageVisitDurationInMilliseconds: Optional[int] = Field(default=None,
                                                                     description="VisitedWebPageVisitDurationInMilliseconds of Document")
    VisitedWebPageContent: Optional[str] = Field(default=None,
                                                 description="Visited WebPage Content in markdown of Document")


# Neo4j connection class
class Neo4jGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def save_to_neo4j(self, doc_meta: DocMeta):
        with self.driver.session() as session:
            session.execute_write(self._create_doc_node, doc_meta)

    @staticmethod
    def _create_doc_node(tx, doc_meta: DocMeta):
        query = (
            "CREATE (d:Document { "
            "BrowsingSessionId: $BrowsingSessionId, "
            "VisitedWebPageURL: $VisitedWebPageURL, "
            "VisitedWebPageTitle: $VisitedWebPageTitle, "
            "VisitedWebPageDateWithTimeInISOString: $VisitedWebPageDateWithTimeInISOString, "
            "VisitedWebPageReffererURL: $VisitedWebPageReffererURL, "
            "VisitedWebPageVisitDurationInMilliseconds: $VisitedWebPageVisitDurationInMilliseconds, "
            "VisitedWebPageContent: $VisitedWebPageContent "
            "})"
        )
        tx.run(query,
               BrowsingSessionId=doc_meta.BrowsingSessionId,
               VisitedWebPageURL=doc_meta.VisitedWebPageURL,
               VisitedWebPageTitle=doc_meta.VisitedWebPageTitle,
               VisitedWebPageDateWithTimeInISOString=doc_meta.VisitedWebPageDateWithTimeInISOString,
               VisitedWebPageReffererURL=doc_meta.VisitedWebPageReffererURL,
               VisitedWebPageVisitDurationInMilliseconds=doc_meta.VisitedWebPageVisitDurationInMilliseconds,
               VisitedWebPageContent=doc_meta.VisitedWebPageContent)


# Function to extract and map data from unstructured text
def parse_unstructured_data(data: str) -> dict:
    # Example regular expressions to extract key information
    session_id = re.search(r'SessionId:\s*(\w+)', data)  # Assuming "SessionId: some_value"
    url = re.search(r'(https?://[^\s]+)', data)  # Find any URL
    title = re.search(r'Title:\s*(.+)', data)  # Assuming "Title: some_title"
    iso_date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', data)  # ISO date format
    referrer_url = re.search(r'Referrer:\s*(https?://[^\s]+)', data)  # Assuming "Referrer: some_url"
    visit_duration = re.search(r'Duration:\s*(\d+)', data)  # Assuming "Duration: some_number"
    content = re.search(r'Content:\s*(.+)', data, re.DOTALL)  # Assuming "Content: some_content"

    # Map the extracted information to a dictionary that matches the Pydantic model
    parsed_data = {
        "BrowsingSessionId": session_id.group(1) if session_id else None,
        "VisitedWebPageURL": url.group(1) if url else None,
        "VisitedWebPageTitle": title.group(1) if title else None,
        "VisitedWebPageDateWithTimeInISOString": iso_date.group(0) if iso_date else None,
        "VisitedWebPageReffererURL": referrer_url.group(1) if referrer_url else None,
        "VisitedWebPageVisitDurationInMilliseconds": int(visit_duration.group(1)) if visit_duration else None,
        "VisitedWebPageContent": content.group(1) if content else None,
    }

    return parsed_data


# Load the unstructured data from the file (from the example)
with open('DataExample.py', 'r') as file:
    unstructured_data = file.read()

# Parse the unstructured data
parsed_data = parse_unstructured_data(unstructured_data)

# Convert the parsed data to the Pydantic model
doc_meta = DocMeta(**parsed_data)

# Save the model into the Neo4j database
graph = Neo4jGraph(uri="bolt://localhost:7687", user="neo4j", password="your_password")
graph.save_to_neo4j(doc_meta)
graph.close()

print("Document saved successfully!")
