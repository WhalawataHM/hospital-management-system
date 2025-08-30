from ..patterns.singleton import DatabaseManager
from typing import Optional, List, TypeVar, Generic, Dict

T = TypeVar('T')

class BaseService(Generic[T]):
    def __init__(self):
        self.db = DatabaseManager.get_instance()

    def _execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        return self.db.execute_query(query, params)

    def _generate_id(self, prefix: str, table: str) -> str:
        query = f"SELECT COUNT(*) as count FROM {table}"
        result = self._execute_query(query)
        count = result[0]['count'] if result else 0
        return f"{prefix}{str(count + 1).zfill(4)}"
