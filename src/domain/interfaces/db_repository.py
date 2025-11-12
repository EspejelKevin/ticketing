from abc import ABCMeta, abstractmethod

from ..schemas.event import EventInput, EventUpdateInput


class DBRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_event_by_id(self, id: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_event_by_name(self, name: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_ticket_by_id(self, id: str):
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
    
    # @abstractmethod
    # def sell_ticket(self, event_id: str):
    #     raise NotImplementedError
    
    # @abstractmethod
    # def exchange_ticket(self, id: str):
    #     raise NotImplementedError

    # @abstractmethod
    # def update_ticket(self, id: str, ticket: dict):
    #     raise NotImplementedError
