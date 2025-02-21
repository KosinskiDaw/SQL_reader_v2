import eventlet
eventlet.monkey_patch() 
from flask import Flask, render_template
from flask_socketio import SocketIO
import lib.generalS7 as generalS7
import lib.conversions as conv
import lib.read_data_plc as plc
import lib.txt_operation as txt_operation
import threading
import time


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

db_param_name = txt_operation.read_lines_config(0)
print(db_param_name)
db_param_var = txt_operation.read_lines_config(1)
print(db_param_var)
db_param_index = txt_operation.read_lines_config(2)
print(db_param_index)
""" --------------------------------------------------------------- """

running = True  


conn = generalS7.connect(IP, rack, slot)
print(f"Connection status: {conn}")



def read_data_from_PLC():
    global conn
    global IP, rack, slot, db_no, start_byte, end_byte
    while running:
        if conn:  
            try:
                # Read request
                read_request = plc.read_data_from_PLC(generalS7, db_no, start_byte, end_byte, conv, "get_bool", 14, 0)
                if read_request is None:
                    # Read connection parameters
                    conn_param = txt_operation.read_lines_conn_param()
                    IP = str(conn_param[0])
                    rack = int(conn_param[1])
                    slot = int(conn_param[2])
                    db_no = int(conn_param[3])
                    start_byte = int(conn_param[4])
                    end_byte = int(conn_param[5])
                    raise Exception("PLC not responding.")
                # Live bit
                socketio.emit('update_data1', {'data': plc.read_data_from_PLC(generalS7, db_no, start_byte, end_byte, conv, "get_bool", 0,0)})
                if read_request is True:
                    socketio.emit('update_data2', {'data': plc.read_data_from_PLC(generalS7, db_no, start_byte, end_byte, conv, "get_dtl", 2,0)})
                    
            except Exception as e:
                print(f"Error reading data from PLC: {str(e)}")
                conn = None  
                generalS7.disconnect()
                print("Disconnected from PLC due to an error.")
        else:
            print("Waiting for reconnection...")
            conn = generalS7.connect(IP, rack, slot)  
            time.sleep(2)  

        time.sleep(2)  

  
    
             

@app.route('/')
def index():
    return render_template('index.html')




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
    
