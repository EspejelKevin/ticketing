from abc import ABCMeta, abstractmethod

from ..schemas.request import EventInput, EventUpdateInput


class DBRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_event_by_id(self, id: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_event_by_name(self, name: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_ticket_by_code(self, code: str):
        raise NotImplementedError
    
    @abstractmethod
    def create_event(self, id: str, event: EventInput):
        raise NotImplementedError
    
    @abstractmethod
    def update_event(self, id: str, event: EventUpdateInput):
        raise NotImplementedError
    
    @abstractmethod
    def delete_event_by_id(self, id: str):
        raise NotImplementedError
    
    @abstractmethod
    def create_ticket(self, ticket: dict):
        raise NotImplementedError

    @abstractmethod
    def update_ticket(self, code: str, ticket: dict):
        raise NotImplementedError
    
    @abstractmethod
    def update_event_tickets_sold(self, id: str, quantity: int):
        raise NotImplementedError
    
    @abstractmethod
    def update_event_tickets_exchanged(self, id: str, quantity: int):
        raise NotImplementedError
