from domain import DBRepository


class DBService(DBRepository):
    def __init__(self, db_repository: DBRepository) -> None:
        self.db_repository = db_repository

    def get_event_by_id(self, id: str):
        return self.db_repository.get_event_by_id(id)
    
    def get_event_by_name(self, name: str):
        return self.db_repository.get_event_by_name(name)
        
    def get_ticket_by_code(self, code: str):
        return self.db_repository.get_ticket_by_code(code)
    
    def create_event(self, id: str, event):
        return self.db_repository.create_event(id, event)
    
    def create_event_historic(self, id: str, event: tuple, current_date):
        return self.db_repository.create_event_historic(id, event, current_date)
    
    def update_event(self, id: str, event):
        return self.db_repository.update_event(id, event)
    
    def delete_event_by_id(self, id: str):
        return self.db_repository.delete_event_by_id(id)
    
    def create_ticket(self, ticket: dict):
        return self.db_repository.create_ticket(ticket)

    def update_ticket(self, code: str, ticket: dict):
        return self.db_repository.update_ticket(code, ticket)

    def update_event_tickets_sold(self, id: str, quantity: int):
        return self.db_repository.update_event_tickets_sold(id, quantity)
    
    def update_event_tickets_exchanged(self, id: str, quantity: int):
        return self.db_repository.update_event_tickets_exchanged(id, quantity)
