# JSTP (JavaScript Transport Protocol) library for Python 3

# Some constants
PACKET_DELIMITER = ',{\f},'
DELIMITER_LENGTH = len(PACKET_DELIMITER)
CHUNKS_FIRST = ['[']
CHUNKS_LAST = [']']
HANDSHAKE_TIMEOUT = 3000
PARSE_TIMEOUT = 30


def deserialize(string):
    """
    Deserialize array of scalar or array of array
    no objects allowed, just arrays and values
    :param string: array serialized to string
    :return: deserialized array
    """
    if string[0] != '[' or string[-1] != ']':
        raise Exception('Incorrect start or end symbols!')

    spliced_parts = split_level(string[1:-1])
    result = []

    for element in spliced_parts:
        res = None
        if element:
            if element[0] == '[':
                res = deserialize(element)
            elif element[0] == '\'' or element[0] == '\"':
                res = parse_string(element)
            elif str.isdigit(element[0]) or element[0] == '-':
                res = parse_number(element)
            elif element[0] == 't' or element[0] == 'f':
                res = parse_boolean(element)
            elif element[0] == 'u' or element[0] == 'n':
                res = parse_none(element)
            result.append(res)
    return result


def parse(string):
    """
    Deserialize string to object, just data: objects and arrays
    no expressions and functions allowed in object definition
    :param string: object serialized to string
    :return: deserialized object
    """
    type_ = None
    if string[0] == '[':
        if string[-1] == ']':
            type_ = 'list'
    elif string[0] == '{':
        if string[-1] == '}':
            type_ = 'dict'
    if type_ is None:
        raise Exception('Incorrect start or end symbols!')

    spliced_parts = split_level(string[1:-1])
    keys = []
    result = []


    if type_ == 'dict':
        tmp = []
        for element in spliced_parts:
            dict_index = string.find(':')
            if dict_index != -1:
                keys.append(element[:dict_index - 1])
                tmp.append(element[dict_index:])
        spliced_parts = tmp

    for element in spliced_parts:
        res = None
        if element:
            if element[0] == '[' or element[0] == '{':
                res = parse(element)
            elif element[0] == '\'' or element[0] == '\"':
                res = parse_string(element)
            elif str.isdigit(element[0]) or element[0] == '-':
                res = parse_number(element)
            elif element[0] == 't' or element[0] == 'f':
                res = parse_boolean(element)
            elif element[0] == 'u' or element[0] == 'n':
                res = parse_none(element)
            result.append(res)

    if type_ == 'dict':
        return compress(keys, result)
    return result


def split_level(string):
    TARGET_SYMBOLS = ['[', '{']
    MIRROR_SYMBOLS = [']', '}']
    count = 0;
    result = []
    last_slice = 0
    for i in range(len(string)):
        if string[i] in TARGET_SYMBOLS:
            count += 1
        elif string[i] in MIRROR_SYMBOLS:
            count -= 1
        if count == 0 and string[i] == ',':
            result.append(string[last_slice:i])
            last_slice = i + 1
    result.append(string[last_slice:])
    return result


def compress(keys, values):
    result = {}
    if len(keys) != len(values):
        raise Exception('Length of objects must be similar!')
    for i in range(len(keys)):
        result[keys[i]] = values[i]
    return result


def parse_string(element):
    if element[0] == element[-1]:
        result = element[1:-1]
        params = [('\\n', '\n'), ('\\\'', '\'')]
        for param in params:
            result = result.replace(*param)
        return result
    else:
        raise Exception('First and last string marker does not similar!')


def parse_number(element):
    try:
        try:
            return int(element)
        except ValueError:
            return float(element)
    except ValueError:
        raise Exception('Incorrect number format!')


def parse_boolean(element):
    element = element.lower()
    if element == 'true':
        return True
    elif element == 'false':
        return False
    else:
        raise ValueError('Incorrect Boolean value!')


def parse_none(element):
    element = element.lower()
    if element == 'undefined' or element == 'null':
        return None
    else:
        raise ValueError('Incorrect None value')


def parse_date(element):
    # TODO in next releases
    pass

