
def read_lines(path):
    data = []
    f = open(path,"r")
    for x in f:
        data.append(x)
    cleaned_data = [line.strip().split() for line in data]
    return cleaned_data
   
path = ("../config/vars.txt")
a = read_lines(path)



print()


# Odczyt danych 
# for i in a:
#     for j in i:
#         print(j)


