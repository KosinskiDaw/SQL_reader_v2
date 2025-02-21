import snap7

plc = snap7.client.Client()

def connect(IP, rack, slot):
    global plc
    if plc.get_connected():  
        print("Already connected to PLC.")
        return True  

    try:
        plc.connect(IP, rack, slot)
        return plc.get_connected()  #
    except Exception as e:
        print(f"Connection to PLC failed: {str(e)}")
        return False  

def disconnect():
    global plc
    if plc.get_connected():
        plc.disconnect()
        print("Disconnected from PLC.")
    return plc.get_connected()  

def read_data(DB_No, start_byte, end_byte):
    return plc.read_area(snap7.type.Areas.DB, DB_No, start_byte, end_byte)

def write_data(DB_No, start_byte, data_to_write):
    plc.db_write(DB_No, start_byte, data_to_write)

