#JSTP lib for Python 3.5.1

# Deserialize array of scalar or array of array
# no objects allowed, just arrays and values
#   string - array serialized to string
#   return - deserialized array
def deserialize(string, index = 0):
    result = []
    index = __skipp_white_spaces(string, index)
    if string[index] != '[':
        return result
    index += 1
    while True:
        index = __skipp_white_spaces(string, index)
        if string[index] == '\'':
            res, index = __parse_string(string, index)
            result.append(res)
        elif str.isdigit(string[index]) or string[index] == '-':
            res, index = __parse_number(string, index)
            result.append(res)
        elif string[index] == '[':
            res, index = deserialize(string, index)
            result.append(res)
        if string[index] == ']':
            index+=1
            return (result, index)
        else:
            index+=1

def parse():
    pass

def interprete():
    pass

def __skipp_white_spaces(string, index):
    while string[index] == ' ' or string[index] == '\t':
        index += 1
    return index

def __parse_string(string, index):
    end_point = ''
    out = ''

    if string[index] == '\'':
        end_point = '\''
    else :
        end_point = '\"'
    index+= 1

    while string[index] != end_point:
        out += string[index]
        index += 1
    index+=1
    return (out, index)

def __parse_number(string, index):
    out = ''

    is_negative = False
    if string[index] == '-':
        is_negative = True
        index+=1

    while str.isdigit(string[index]) or string[index] == '.':
        out += string[index]
        index += 1

    try:
        res = int(out)
    except ValueError:
        res = float(out)
    if is_negative:
        res = 0 - res
    return (res, index)
