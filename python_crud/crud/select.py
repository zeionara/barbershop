def select(cursor, table_name, columns_to_show, columns_to_check, values_to_check):
    checking_chain = ""
    showing_chain = ""
    if (len(columns_to_show) == 0):
        columns_to_show.append("*")
    for i in range(len(columns_to_show)):
        if showing_chain == "":    
            showing_chain = showing_chain + columns_to_show[i]
        else:
            showing_chain = showing_chain + ", " + columns_to_show[i]
    if (len(columns_to_check) == 0):
        return cursor.execute("select %s from %s" % (showing_chain, table_name))
    for i in range(len(columns_to_check)):
        if checking_chain == "":    
            checking_chain = checking_chain + columns_to_check[i] + " = " + values_to_check[i]
        else:
            checking_chain = checking_chain + " and " + columns_to_check[i] + " = " + values_to_check[i]
    print("select %s from %s where %s" % (showing_chain, table_name, checking_chain))
    return cursor.execute("select %s from %s where %s" % (showing_chain, table_name, checking_chain))
