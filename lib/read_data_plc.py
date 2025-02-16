def read_data_from_PLC(generalS7,db_no, start_byte, end_byte, conv, var_type, var_byte):
    try:
            data = generalS7.read_data(db_no, start_byte, end_byte)
            print(f"Raw data: {data}")
            method_to_call = getattr(conv, var_type)
            converted_data = method_to_call(data, var_byte)
            print(f"Converted data: {converted_data}")
            return converted_data
    except Exception as e:
        print(f"Error reading data from PLC: {str(e)}")
 