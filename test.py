import binascii

def str_to_hexStr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')

def hexStr_to_str(hex_str):
    hex = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hex)
    return str_bin.decode('utf-8')

str1 = 0x1d6152ee93dd4122beb14c307e1779224f7e21b84aefc066549bd3847f15d5b699fd9570c5e7f1227e8c2a9f30cae335d4eb796dabe90d66e75fcea16000a1caf3295ac13ffa3f1b3a3b57377c18901f2f40d6bbaf5fb528100ead418648ed7ce57edaad8c
hex1 = hexStr_to_str(str1)
print(hex1)
print(type(hex1))