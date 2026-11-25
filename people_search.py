from abc import ABC, abstractmethod
from database import search_people


# Defines what a people search must be able to do
class PeopleSearchSource(ABC):

    @abstractmethod
    def search(self, name_or_id):
        pass


# Searches for people using our SQLite database
class SQLitePeopleSearch(PeopleSearchSource):

    def search(self, name_or_id):
        return search_people(name_or_id)


# Using a search source provided by another part of the program
class PeopleSearchService:

    def __init__(self, source):
        self.source = source

    def find(self, name_or_id):
        return self.source.search(name_or_id)
