import snap7

plc = snap7.client.Client()
def connect(IP, rack, slot):
    try:
        plc.connect(IP, rack, slot)
    except Exception as e:
        print(f"Connection to PLC failed: {str(e)}")
        return False

    return plc.get_connected()

def disconnect():
    plc.disconnect()
    return plc.get_connected()

def read_data(DB_No, start_byte, end_byte):
    return plc.read_area(snap7.type.Areas.DB, DB_No, start_byte, end_byte)

