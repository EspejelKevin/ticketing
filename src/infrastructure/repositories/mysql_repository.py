from domain import DBRepository
from log import Log


class MySQLRepository(DBRepository):
    def __init__(self, database, log: Log) -> None:
        self.database = database
        self.log = log

    def get_event_by_id(self, id: str):
        with self.database() as mysql:
            session = mysql.get_session()
            cursor = session.cursor()
            query = 'SELECT name, start_date, end_date, total_tickets, total_tickets_sold, total_tickets_exchange FROM events WHERE id=%s'
            cursor.execute(query, (id,))
            self.log.info('consuming get_event_by_id', extra={'details': {'query_sql': query, 'data': id}})
            return cursor.fetchone()
    
    def get_event_by_name(self, name: str):
        with self.database() as mysql:
            session = mysql.get_session()
            cursor = session.cursor()
            query = 'SELECT * FROM events WHERE name=%s'
            cursor.execute(query, (name,))
            self.log.info('consuming get_event_by_name', extra={'details': {'query_sql': query, 'data': name}})
            return cursor.fetchone()
        
    def get_ticket_by_code(self, code: str):
        with self.database() as mysql:
            session = mysql.get_session()
            cursor = session.cursor()
            query = 'SELECT * FROM tickets WHERE code=%s'
            cursor.execute(query, (code,))
            self.log.info('consuming get_ticket_by_code', extra={'details': {'query_sql': query, 'data': code}})
            return cursor.fetchone()
    
    def create_event(self, id: str, event):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                query = 'INSERT INTO events(id, name, start_date, end_date, total_tickets) VALUES(%s, %s, %s, %s, %s)'
                data = (id, event.name, event.start_date, event.end_date, event.total_tickets)
                cursor.execute(query, data)
                self.log.info('consuming create_event', extra={'details': {'query_sql': query, 'data': data}})
                return cursor.rowcount > 0
        except Exception:
            self.log.error('error on create_event', exc_info=True)
            return False
    
    def update_event(self, id: str, event):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                query = 'UPDATE events SET name=%s, start_date=%s, end_date=%s, total_tickets=%s WHERE id=%s'
                data = (event.name, event.start_date, event.end_date, event.total_tickets, id)
                cursor.execute(query, data)
                self.log.info('consuming update_event', extra={'details': {'query_sql': query, 'data': data}})
                return cursor.rowcount > 0
        except Exception:
            self.log.error('error on update_event', exc_info=True)
            return None
    
    def delete_event_by_id(self, id: str):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                query = 'DELETE FROM events WHERE id=%s'
                cursor.execute(query, (id,))
                self.log.info('consuming delete_event_by_id', extra={'details': {'query_sql': query, 'data': id}})
                return cursor.rowcount > 0
        except Exception:
            self.log.error('error on delete_event_by_id', exc_info=True)
            return False

    def create_ticket(self, ticket: dict):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                query = 'INSERT INTO tickets(id, code, sale_date, event_id) VALUES(%s, %s, %s, %s)'
                data = (ticket['id'], ticket['code'], ticket['sale_date'], ticket['event_id'])
                cursor.execute(query, data)
                self.log.info('consuming create_ticket', extra={'details': {'query_sql': query, 'data': data}})
                return cursor.rowcount > 0
        except Exception:
            self.log.error('error on create_ticket', exc_info=True)
            return False

    def update_ticket(self, code: str, ticket: dict):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                query = 'UPDATE tickets SET exchange=%s, exchange_date=%s WHERE code=%s'
                data = (ticket['exchange'], ticket['exchange_date'], code)
                cursor.execute(query, data)
                self.log.info('consuming update_ticket', extra={'details': {'query_sql': query, 'data': data}})
                return cursor.rowcount > 0
        except Exception:
            self.log.error('error on update_ticket', exc_info=True)
            return None
        
    def update_event_tickets_sold(self, id: int, quantity: int):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                query = 'UPDATE events SET total_tickets_sold=%s WHERE id=%s'
                data = (quantity, id)
                cursor.execute(query, data)
                self.log.info('consuming update_event_tickets_sold', extra={'details': {'query_sql': query, 'data': data}})
                return cursor.rowcount > 0
        except Exception:
            self.log.error('error on update_event_tickets_sold', exc_info=True)
            return None
        
    def update_event_tickets_exchanged(self, id: str, quantity: int):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                query = 'UPDATE events SET total_tickets_exchange=%s WHERE id=%s'
                data = (quantity, id)
                cursor.execute(query, data)
                self.log.info('consuming update_event_tickets_exchanged', extra={'details': {'query_sql': query, 'data': data}})
                return cursor.rowcount > 0
        except Exception:
            self.log.error('error on update_event_tickets_exchanged', exc_info=True)
            return None
