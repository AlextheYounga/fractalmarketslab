# Returns a list of items from a nested object.
def extractData(data, key):
    values = []
    if (type(key) == list):
        if len(key) == 2:
            for i, row in data.items():
                value = float(row[key[0]][key[1]])
                values.append(value)
        if len(key) == 3:
            for i, row in data.items():
                value = float(row[key[0]][key[1]][key[2]])
                values.append(value)
        if len(key) == 4:
            for i, row in data.items():
                value = float(row[key[0]][key[1]][key[2]][key[3]])
                values.append(value)
        if len(key) == 5:
            for i, row in data.items():
                value = float(row[key[0]][key[1]][key[2]][key[3]][key[4]])
                values.append(value)
        if len(key) > 5:
            return 'Nest level too deep to retrieve via function.'
    else:
        for i, row in data.items():
            value = float(row[key])
            values.append(value)
    return values