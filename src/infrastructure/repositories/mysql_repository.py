from domain import DBRepository


class MySQLRepository(DBRepository):
    def __init__(self, database) -> None:
        self.database = database

    def get_event_by_id(self, id: str):
        with self.database() as mysql:
            session = mysql.get_session()
            cursor = session.cursor()
            cursor.execute(
                '''SELECT name, start_date, end_date, 
                          total_tickets, total_tickets_sold, 
                          total_tickets_exchange 
                   FROM events WHERE id=%s''',
                (id,)
            )
            return cursor.fetchone()
    
    def get_event_by_name(self, name: str):
        with self.database() as mysql:
            session = mysql.get_session()
            cursor = session.cursor()
            cursor.execute(
                'SELECT * FROM events WHERE name=%s',
                (name,)
            )
            return cursor.fetchone()
        
    def get_ticket_by_code(self, code: str):
        with self.database() as mysql:
            session = mysql.get_session()
            cursor = session.cursor()
            cursor.execute(
                'SELECT * FROM tickets WHERE code=%s',
                (code,)
            )
            return cursor.fetchone()
    
    def create_event(self, id: str, event):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                cursor.execute(
                    'INSERT INTO events(id, name, start_date, end_date, total_tickets) VALUES(%s, %s, %s, %s, %s)',
                    (id, event.name, event.start_date, event.end_date, event.total_tickets)
                )
                return cursor.rowcount > 0
        except Exception:
            return False
    
    def update_event(self, id: str, event):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                cursor.execute(
                    'UPDATE events SET name=%s, start_date=%s, end_date=%s, total_tickets=%s WHERE id=%s',
                    (event.name, event.start_date, event.end_date, event.total_tickets, id)
                )
                return cursor.rowcount > 0
        except Exception:
            return None
    
    def delete_event_by_id(self, id: str):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                cursor.execute(
                    'DELETE FROM events WHERE id=%s',
                    (id,)
                )
                return cursor.rowcount > 0
        except Exception:
            return False

    def create_ticket(self, ticket: dict):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                cursor.execute(
                    'INSERT INTO tickets(id, code, sale_date, event_id) VALUES(%s, %s, %s, %s)',
                    (ticket['id'], ticket['code'], ticket['sale_date'], ticket['event_id'])
                )
                return cursor.rowcount > 0
        except Exception:
            return False

    def update_ticket(self, code: str, ticket: dict):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                cursor.execute(
                    'UPDATE tickets SET exchange=%s, exchange_date=%s WHERE code=%s',
                    (ticket['exchange'], ticket['exchange_date'], code)
                )
                return cursor.rowcount > 0
        except Exception:
            return None
        
    def update_event_tickets_sold(self, id: int, quantity: int):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                cursor.execute(
                    'UPDATE events SET total_tickets_sold=%s WHERE id=%s',
                    (quantity, id)
                )
                return cursor.rowcount > 0
        except Exception:
            return None
        
    def update_event_tickets_exchanged(self, id: str, quantity: int):
        try:
            with self.database() as mysql:
                session = mysql.get_session()
                cursor = session.cursor()
                cursor.execute(
                    'UPDATE events SET total_tickets_exchange=%s WHERE id=%s',
                    (quantity, id)
                )
                return cursor.rowcount > 0
        except Exception:
            return None
