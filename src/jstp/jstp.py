# JSTP (JavaScript Transport Protocol) library for Python 3

PACKET_DELIMITER = ',{\f},'
DELIMITER_LENGTH = len(PACKET_DELIMITER)
CHUNKS_FIRST = ['[']
CHUNKS_LAST = [']']
HANDSHAKE_TIMEOUT = 3000


def deserialize(string, index=0):
    """
    Deserialize array of scalar or array of array
    no objects allowed, just arrays and values
    :param string: array serialized to string
    :param index: current position in string
    :return: deserialized array
    """
    if string[index] != '[':
        return []
    result = []
    index += 1

    while True:
        if string[index] == '\'':
            res, index = __parse_string(string, index)
        elif str.isdigit(string[index]) or string[index] == '-':
            res, index = __parse_number(string, index)
        elif string[index] == 't' or string[index] == 'f':
            res, index = __parse_boolean(string, index)
        elif string[index] == 'u':
            res, index = __parse_undefined(string, index)
        elif string[index] == '[':
            res, index = deserialize(string, index)
        result.append(res)

        if string[index] == ']':
            index += 1
            if index == len(string):
                return result
            return result, index
        else:
            index += 1


def parse(string, index=0):
    """
    Deserialize string to object, just data: objects and arrays
    no expressions and functions allowed in object definition
    :param string: object serialized to string
    :param index: current position in string
    :return: deserialized object
    """
    if string[index] == '{':
        result = {}
        type_ = 'dict'
    elif string[index] == '[':
        result = []
        type_ = 'array'
    else:
        return {}
    key = 0
    index += 1

    while True:
        if string[index] == '\'':
            res, index = __parse_string(string, index)
        elif str.isdigit(string[index]) or string[index] == '-':
            res, index = __parse_number(string, index)
        elif string[index] == 't' or string[index] == 'f':
            res, index = __parse_boolean(string, index)
        elif string[index] == '[' or string[index] == '{':
            res, index = parse(string, index)
        result, key = __append(result, res, type_, key)

        if string[index] == ']' or string[index] == '}':
            index += 1
            if index == len(string):
                return result
            return result, index
        else:
            index += 1


def __skipp_white_spaces(string, index):
    while string[index] == ' ' or string[index] == '\t':
        index += 1
    return index


def __append(result, res, type_, key):
    if type_ == 'dict':
        result[key] = res
        key += 1
    else:
        result.append(res)
    return result, key


def __parse_string(string, index):
    if string[index] == '\'':
        end_point = '\''
    else:
        end_point = '\"'
    index += 1
    start = index

    while string[index] != end_point:
        index += 1
    index += 1

    return string[start:index-1], index


def __parse_number(string, index):
    is_negative = False
    if string[index] == '-':
        is_negative = True
        index += 1
    start = index

    while str.isdigit(string[index]) or string[index] == '.':
        index += 1

    try:
        res = int(string[start:index])
    except ValueError:
        res = float(string[start:index])
    if is_negative:
        res = 0 - res
    return res, index


def __parse_boolean(string, index):
    if string[index: index + 4] == 'true':
        return True, index + 4
    elif string[index: index + 5] == 'false':
        return False, index + 5
    else:
        return None, index


def __parse_undefined(string, index):
    if string[index: index + 9] == 'undefined':
        return None, index + 9
    else:
        return None, index