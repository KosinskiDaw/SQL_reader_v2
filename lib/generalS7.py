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

def write_data(DB_No, start_byte, end_byte):
    """Writes a data area into a PLC.

        Args:
            area: area to be written.
            db_number: number of the db to be written to. In case of Inputs, Marks or Outputs, this should be equal to 0
            start: byte index to start writting.
            data: buffer to be written.

        Returns:
            Snap7 error code.

        Exmaple:
            >>> from util.db import DB
            >>> import snap7
            >>> client = snap7.client.Client()
            >>> client.connect("192.168.0.1", 0, 0)
            >>> buffer = bytearray([0b00000001])
            # Writes the bit 0 of the byte 10 from the DB number 1 to TRUE.
            >>> client.write_area(DB, 1, 10, buffer)
        """
    plc.write_area()

