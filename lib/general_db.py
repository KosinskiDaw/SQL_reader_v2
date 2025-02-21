import sqlite3



def conn_to_sqlite():
    conn = sqlite3.connect("process_values")
    return conn

def create_table(columns):
    columns_sql = ", ".join(columns)
    c = conn_to_sqlite()
    c.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS process_values
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              {columns_sql})''')
    
def add_column(column):
    # Brak możliwości dodawania wielu koumn na raz
    c = conn_to_sqlite()
    c.cursor()
    c.execute(f"ALTER TABLE process_values ADD COLUMN {column}")

def conn_close():
    conn_to_sqlite().commit()
    conn_to_sqlite().close()

# columns = ["test1, test2, test3"]  
# create_table(columns)
# column = "xd"
# add_column(column)
# conn_close()
