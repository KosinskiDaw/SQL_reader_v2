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
import snap7

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')  
""" ------------------------ Parameters --------------------------- """
conn_param = txt_operation.read_lines_conn_param()
print(conn_param)
IP = str(conn_param[0])
rack = int(conn_param[1])
slot = int(conn_param[2])
db_no = int(conn_param[3])
start_byte = int(conn_param[4])
end_byte = int(conn_param[5])
""" --------------------------------------------------------------- """

running = True  

 



conn = generalS7.connect(IP, rack, slot)
print(f"Connection status: {conn}")



def read_data_from_PLC(): 
    try:
        global conn
        while running and conn: 
        # Emitowanie danych do klienta przez SocketIO
   
            socketio.emit('update_data1', {'data': plc.read_data_from_PLC(generalS7, db_no, start_byte, end_byte, conv, "get_real", 2)})
            socketio.emit('update_data2', {'data': plc.read_data_from_PLC(generalS7, db_no, start_byte, end_byte, conv, "get_real", 6)})
            time.sleep(2)
    except Exception as e:
        print(f"Error reading data from PLC: {str(e)}")
    finally:
        if conn:
            generalS7.disconnect()
            print("Disconnected from PLC.")

def check_connection():
        global conn
        while True:
             if conn:
                print(f"Connection status: {conn}")
                time.sleep(2)
             else:
                conn = generalS7.connect(IP, rack, slot)
                print(f"Connection status: {conn}")
                time.sleep(2)
        
    
        
    
             

@app.route('/')
def index():
    return render_template('index.html')




if __name__ == "__main__":
    # if conn:
    data_thread = threading.Thread(target=read_data_from_PLC, daemon=True)
    data_thread.start()
    conn_thread = threading.Thread(target=check_connection,daemon=True)
    conn_thread.start()

    try:
    
            socketio.run(app, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
            print("\nProgram zakończony za pomocą Ctrl+C.")
    finally:
            
            running = False
            
            data_thread.join()
            conn_thread.join()
            print("Wątek zakończył działanie.")

            socketio.stop()
            print("SocketIO zatrzymane.")
    
