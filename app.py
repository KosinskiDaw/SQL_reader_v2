from flask import Flask, render_template
from flask_socketio import SocketIO
import lib.generalS7 as generalS7
import lib.conversions as conv
import lib.read_data_plc as plc
import threading
import time
import eventlet

eventlet.monkey_patch()  

""" ------------------------ Parameters --------------------------- """
IP = "192.168.10.150"
rack = 0
slot = 1
db_no = 3291
start_byte = 0
end_byte = 100
""" --------------------------------------------------------------- """

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')  
running = True  


conn = generalS7.connect(IP, rack, slot)
print(f"Connection status: {conn}")

def read_data_from_PLC(): 
    try:
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

        socketio.stop()
        print("SocketIO zatrzymane.")
