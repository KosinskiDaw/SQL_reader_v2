import eventlet
eventlet.monkey_patch() 
from flask import Flask, render_template
from flask_socketio import SocketIO
import lib.generalS7 as generalS7
import lib.conversions as conv
import lib.read_data_plc as plc
import lib.txt_operation as txt_operation
import lib.general_db as general_db
import threading
import time
import json


app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')  
""" ------------------------ Parameters --------------------------- """
conn_param = txt_operation.read_lines_conn_param()
IP = str(conn_param[0])
rack = int(conn_param[1])
slot = int(conn_param[2])
db_no = int(conn_param[3])
start_byte = int(conn_param[4])
end_byte = int(conn_param[5])
""" --------------------------------------------------------------- """

running = True  


conn = generalS7.connect(IP, rack, slot)
# print(f"Connection status: {conn}")

def build_structure_name():
    db_param_name = txt_operation.read_lines_config(0)
    return db_param_name
def build_structure_var():
    db_param_var = txt_operation.read_lines_config(1)
    return db_param_var

def build_structure_index():
    db_param_index = txt_operation.read_lines_config(2)
    return db_param_index

def read_data_from_PLC():
    global conn
    global IP, rack, slot, db_no, start_byte, end_byte
    name = []
    var = []
    index = []

    for i in range(len(build_structure_name())):
        name.append(str(build_structure_name()[i].strip().lower()))
    for i in range(len(build_structure_var())):
        var.append(str(build_structure_var()[i].strip().lower()))
    for i in range(len(build_structure_index())):
        index.append(int(str(build_structure_index()[i].strip().split('.')[0])))



    
    
    while running:
        db_conn = general_db.conn_to_sqlite()
        print(name)
        general_db.create_table(name)
        if conn:  
            try:
                # Read request
                read_request = plc.read_data_from_PLC(generalS7, db_no, start_byte, end_byte, conv, "get_bool", 14, 0)
                if read_request is None:
                    raise Exception("PLC not responding.")
                # Live bit
                socketio.emit('live_bit', {'data': plc.read_data_from_PLC(generalS7, db_no, start_byte, end_byte, conv, "get_bool", 0,0)})

                if read_request is True:
                    data =[]
                    data.clear()
                    #  Tutaj będą dane odczytywane z PLC i zapisywane do sql po wystawieniu przez PLC request
                    for i in range(1,len(build_structure_index())):
                        socketio.emit(f'update_data{i}', {'data': plc.read_data_from_PLC(generalS7, db_no, start_byte, end_byte, conv, f"get_{var[i]}", index[i],0)})
                        data.append(plc.read_data_from_PLC(generalS7, db_no, start_byte, end_byte, conv, f"get_{var[i]}", index[i],0))
                    print(data)
                   
                    # Delete request 
                    generalS7.write_data(db_no, 14, bytearray([0]))
                    
            except Exception as e:
                print(f"Error reading data from PLC: {str(e)}")
                conn = None
                IP = None
                rack = None
                slot = None
                db_no = None
                start_byte = None
                end_byte = None 
                generalS7.disconnect()
                print("Disconnected from PLC due to an error.")
        else:
            print("Waiting for reconnection...")
            conn_param = txt_operation.read_lines_conn_param()
            IP = str(conn_param[0])
            rack = int(conn_param[1])
            slot = int(conn_param[2])
            db_no = int(conn_param[3])
            start_byte = int(conn_param[4])
            end_byte = int(conn_param[5])
            conn = generalS7.connect(IP, rack, slot)  
            time.sleep(2)  

        time.sleep(0.3)  

  
    
             

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return render_template('table_window.html')

@app.route('/data/get', methods=['GET'])
def get():
    conn = general_db.conn_to_sqlite()
    cursor = conn.cursor()
    # Pobierz dane
    cursor.execute('SELECT * process_values')
    data = cursor.fetchall() 
    # Pobierz nazwy kolumn w kolejności
    column_names = [description[0] for description in cursor.description]
    json_data = [dict(zip(column_names, row)) for row in data]
    conn.close()
    # Przygotuj dane w odpowiednim formacie
    return jsonify({"columns": column_names, "data": json_data})



if __name__ == "__main__":
    data_thread = threading.Thread(target=read_data_from_PLC, daemon=True)
    data_thread.start()


    try:
    
            socketio.run(app, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
            print("\nProgram zakończony za pomocą Ctrl+C.")
    finally:
            
            running = False
            
            data_thread.join()
            print("Wątek zakończył działanie.")
            generalS7.disconnect()
            socketio.stop()
            print("SocketIO zatrzymane.")
    
