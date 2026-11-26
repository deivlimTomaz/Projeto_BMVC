from app.controllers.sqlite_store import SQLiteStore

class DataRecord(SQLiteStore):

    # DataRecord gerencia a persistência dos produtos usando SQLiteStore

    def __init__(self, caminho_db=None):
        super().__init__(caminho_db)
