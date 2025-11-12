from domain import DBRepository


class DBService(DBRepository):
    def __init__(self, db_repository: DBRepository) -> None:
        self.db_repository = db_repository

    def get_event_by_id(self, id: str):
        return self.db_repository.get_event_by_id(id)
    
    def get_event_by_name(self, name: str):
        return self.db_repository.get_event_by_name(name)
        
    def get_ticket_by_id(self, id: str):
        return self.db_repository.get_ticket_by_id(id)
    
    def create_event(self, id: str, event):
        return self.db_repository.create_event(id, event)
    
    def update_event(self, id: str, event):
        return self.db_repository.update_event(id, event)
    
    def delete_event_by_id(self, id: str):
        return self.db_repository.delete_event_by_id(id)
