import parameter_getters

def get_column_by_index(columns, index):
    for column in columns:
        if (column[4] == index):
            return column





columns = (("id", "-i", "int", 10, 2, -2), ("name","-n", "str", 100, 3, 1), ("price","-p","int", 15, 0, -1), ("quantity","-q","int", 15, 1, 2))
command = ["upd","name_new","100"]
col = 0
#print(iterator_insert(columns, command, col))
print(get_insert_template(columns))
