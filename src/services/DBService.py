import sqlite3

class SQLiteWrapper:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_contract_table(self):
        self.connect()
        query = '''
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY,
                contract_id TEXT,
                network INTEGER
            );
        '''
        self.cursor.execute(query)
        self.conn.commit()
        

    def create_product_table(self):
        self.connect()
        query = '''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                category TEXT,
                name TEXT,
                binpath TEXT,
                callable TEXT,
                contract_id TEXT,
                instantiated BOOL DEFAULT false,
                evm_addr TEXT,
                contract_index INTEGER
            );
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def insert_product(self, category, name, binpath, callable_func, contract_id):
        self.connect()
        query = '''
            INSERT INTO products (category, name, binpath, callable, contract_id)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (category, name, binpath, callable_func, contract_id))
        self.conn.commit()
        last_row_id = self.cursor.lastrowid
        return last_row_id

    def insert_contract(self, contract_id, network):
        self.connect()
        query = '''
          INSERT INTO contracts (contract_id, network)
          VALUES (?, ?)
        '''

        self.cursor.execute(query, (contract_id, network))
        self.conn.commit()
        last_row_id = self.cursor.lastrowid
        return last_row_id


# Example usage
#wrapper = SQLiteWrapper('your_database.db')
#wrapper.create_table()
#wrapper.insert_product('Model', 'Model H', './contract_bytecode/models/model_h.bin', 'retrieve_model_dict', '0.0.14973364')
