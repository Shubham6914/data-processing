from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
#  Pydantic models for data validation before processing
class JournalInfo(BaseModel):
    title: str
    issn: str
    issue: Optional[str]
    volume: Optional[str]

class PublicationDate(BaseModel):
    year: str
    month: Optional[str]
    day: Optional[str]

class BasicInfo(BaseModel):
    pmid: str
    publication_date: PublicationDate
    journal: JournalInfo

class Author(BaseModel):
    last_name: str
    fore_name: str
    affiliations: List[str] = []

class AbstractSection(BaseModel):
    label: Optional[str]
    nlm_category: Optional[str]
    text: str

class Content(BaseModel):
    title: str
    abstract: List[AbstractSection]
    authors: List[Author]
    keywords: List[str] = []

class Metadata(BaseModel):
    doi: Optional[str]
    references: List[str] = []

class MedicalArticle(BaseModel):
    basic_info: BasicInfo
    content: Content
    metadata: Metadata
    extracted_at: datetime