from db import Db

from auth import Auth

class Call:
    def __init__(self, date_and_time, note, call_id=None, customer_id=None, user_id=None):
        self.call_id = call_id
        self.customer_id = customer_id
        self.user_id = user_id
        self.date_and_time = date_and_time
        self.note = note

    def save(self):
        '''If self has been populated by database data - UPDATE.
        Otherwise - INSERT a new record.'''
        db = Db()
        data = (self.date_and_time, self.note, self.call_id, self.customer_id, self.user_id)
        query = "INSERT INTO phone_call VALUES (?, ?, ?, ?, ?)"
        db.execute(query, data)
        db.commit()

    def build_from_row(row):
        if row is None:
            return None
        call = Call(row[0], row[1], row[2], row[3], row[4])
        return call

    # Note: this is a CLASS function (no self!)
    def get_for_customer(customer_id, include_user=False):
        '''Return a list of Call objects for the given customer.
        (Bonus: if include_user is True, add a 'user' attribute/property
        to each Call object, containing all the info about the user who
        created the Call object.)'''
        db = Db()
        if include_user == True:
            query =  '''SELECT * from phone_call
                    JOIN user
                    ON user.user_id = phone_call.user_id
                    WHERE customer_id = ?
                    AND phone_call.user_id = ?
                    ORDER BY phone_call.date_and_time DESC'''
            db.execute(query, (customer_id, include_user))
            calls = db.fetchall()
        else:
            query =  "SELECT * from phone_call WHERE customer_id = ?"
            db.execute(query, (customer_id,))
            calls = db.fetchall()
        return calls

    def get(call_id):
        '''Get a single Call object that corresponds to the call id.
        If none found, return None.'''
        db = Db()
        query = "SELECT * from phone_call WHERE call_id = ?"
        db.execute(query, (call_id,))
        call = db.fetchone()
        if call is not None:
            return call
        else:
            return None

    # Note: this is a CLASS function (no self!)
    def get_all():
        '''Get a list of Call objects - one for each row in the 
        relevant table in the database.'''
        db = Db()
        query = "SELECT * from phone_call"
        db.execute(query)
        phone_calls = db.fetchall()
        return phone_calls
