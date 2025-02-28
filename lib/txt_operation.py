
def read_lines_config(value):
    # path = ("../config/vars.txt")
    path = ("config/vars.txt")
    data = []
    index = []
    transformed_data = []
    try:
        f = open(path,"r")
        for x in f:
            data.append(x)
        cleaned_data = [line.strip().split() for line in data]
        f.close()
        data.clear()
        
        l = len(cleaned_data)

        for i in range(0, l):
            for j in cleaned_data:
                if "Struct" in cleaned_data[i]:
                    index.append(i)
                    break
                elif "Array" in cleaned_data[i]:
                    index.append(i)
                    break
        ix = len(index)
        c = 0
        for i in range(0,ix):
            a = index[i]
            b = a - c
            cleaned_data.pop(b)
            c = c + 1

        for i in cleaned_data:
            for j in i:
                data.append(j)
        for k in range(value, len(data), 3):
            transformed_data.append(data[k])
        
        return transformed_data

    except Exception as e:
        print(f"Error reading data from file: {str(e)}")
        return False
    

def read_lines_conn_param():
    path = ("../config/con_param.txt")
    path = ("config/con_param.txt")
    data = []
    transformed_data = []
    try:
        f = open(path,"r")
        for x in f:
            data.append(x)
        cleaned_data = [line.strip().split() for line in data]
        data.clear()
        for i in cleaned_data:
            for j in i:
                data.append(j)
        for k in range(1, len(data),2):
            transformed_data.append(data[k])
        f.close()
        return transformed_data
    except Exception as e:
        print(f"Error reading data from file: {str(e)}")
        return False  

# # a = read_lines_config(0)
# a = read_lines_conn_param()
# print(a[0])
# print("----------------------------")
# # a = read_lines_config(1)
# print(a[1])
# print("----------------------------")
# # a = read_lines_config(2)
# print(a[2])


