import json
from pydantic import BaseModel, Field
from typing import Optional

# Define the Pydantic model
class DocMeta(BaseModel):
    BrowsingSessionId: Optional[str] = Field(default=None, description="BrowsingSessionId of Document")
    VisitedWebPageURL: Optional[str] = Field(default=None, description="VisitedWebPageURL of Document")
    VisitedWebPageTitle: Optional[str] = Field(default=None, description="VisitedWebPageTitle of Document")
    VisitedWebPageDateWithTimeInISOString: Optional[str] = Field(default=None, description="VisitedWebPageDateWithTimeInISOString of Document")
    VisitedWebPageReffererURL: Optional[str] = Field(default=None, description="VisitedWebPageReffererURL of Document")
    VisitedWebPageVisitDurationInMilliseconds: Optional[int] = Field(default=None, description="VisitedWebPageVisitDurationInMilliseconds of Document")
    VisitedWebPageContent: Optional[str] = Field(default=None, description="Visited WebPage Content in markdown of Document")

# Load JSON data (assuming DataExample.py contains JSON content)
with open('DataExample.py', 'r') as file:
    json_data = json.load(file)

# Convert JSON to Pydantic model
doc_meta = DocMeta(**json_data)

# Now doc_meta is a fully validated Python object based on the Pydantic model
print(doc_meta)
