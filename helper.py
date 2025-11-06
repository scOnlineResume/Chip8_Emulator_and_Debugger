# Takes number in integer format, then returns first digit of the hex string
# in string format
def extract_first_digit_s(one_byte_number):
    _nString = pad_hex_string(str(hex(one_byte_number))[2:])
    _firstString = _nString[0]
    return _firstString

# Takes number in integer format, then returns second digit of the hex string
# in string format
def extract_second_digit_s(one_byte_number):
    _nString = pad_hex_string(str(hex(one_byte_number))[2:])
    _secondString = _nString[1]
    return _secondString

# Takes number in integer format, then returns first digit of the hex number
# in integer format
def extract_first_digit_int(one_byte_number):
    _nString = pad_hex_string(str(hex(one_byte_number))[2:])
    _firstString = _nString[0]
    return int(_firstString)

# Takes number in integer format, then returns second digit of the hex string
# in string format
def extract_second_digit_int(one_byte_number):
    _nString = pad_hex_string(str(hex(one_byte_number))[2:])
    _secondString = _nString[1]
    return int(_secondString)

def pad_hex_string(hex_string):
    if len(hex_string) == 1:
        return "0" + hex_string
    else:
        return hex_string



##### BITWISE OPERATIONS #####
def get_nth_bit(number,n):
    # Return the nth bit
    return (number & (1 << (7-n))) >> (7-n)
    

##### Digit Extraction #####
def extract_digits(number):
    # In the form (d1)(d2)(d3)
    d1 = number // 100
    d3 = number % 10
    d2 = (number - (d1*100) - d3) // 10

    return d1,d2,d3
