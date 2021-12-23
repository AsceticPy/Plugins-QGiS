query_file = "data/raz_export.txt"

with open(query_file, "r") as data_file:
        query_list: str = []
        while True:
            line0 = data_file.readline()

            if not line0:
                break
            query_list.append(data_file.readline().strip())
            #query_list.append(str(line.strip() in line for line in data_file))

for l in query_list:
    print(l)