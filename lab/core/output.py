import texttable
from tabulate import tabulate
import sys


def setWidths(data, w='default'):
    """ 
    Parameters
    ----------
    data :  dict|list
    """
    if (w == 'default'):
        w = 3
    if (type(data) == dict):
        widths = []
        for word in data.keys():
            length = len(word)
            if ((w != 3) or (length < 5)):
                length = length * w
            widths.append(length)
        return widths
    if (type(data) == list):
        widths = []
        for word in data:
            length = len(word)
            if ((w != 3) or (length < 5)):
                length = length * w
            widths.append(length)
        return widths
    return False


def printFullTable(data, widths='default'):
    """ 
    Parameters
    ----------
    data :  dict
    """
    print("\n")
    table = texttable.Texttable()
    if (type(data) == list):
        headers = data.pop(0)
        table.header(headers)
        table.set_cols_width(setWidths(headers, widths))
        for r in data:
            table.add_rows([r], header=False)

    print(table.draw())


def printTable(data, widths='default'):
    """ 
    Parameters
    ----------
    data :  dict
    """
    print("\n")
    headers = data.keys()
    table = texttable.Texttable()
    table.header(headers)
    table.set_cols_width(setWidths(data, widths))
    table.add_rows([data.values()], header=False)

    print(table.draw())


def printTabs(data, tablefmt):
    tabdata = []
    if (type(data) == dict):
        for h, v in data.items():
            tabrow = [h, v]
            tabdata.append(tabrow)
        print(tabulate(tabdata))
    if (type(data) == list):
        tabdata = data
        print(tabulate(tabdata, tablefmt))


def drawBox(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)


def listTable(data):
    dash = '-' * 40
    for i in range(len(data)):
        if i == 0:
            print(dash)
            print('{:<10s}{:>4s}{:>12s}'.format(data[i][0], data[i][1], data[i][2]))
            print(dash)
        else:
            print('{:<10s}{:>4s}{:>12.1f}'.format(data[i][0], data[i][1], data[i][2]))