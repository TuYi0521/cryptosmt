'''
Created on Mar 28, 2014

@author: stefan
'''

from cryptanalysis import diffchars
import re


def getCharBoolectorOutput(output, char_format, rounds):
    """
    Parse the output of Boolector and construct a characteristic.
    """
    characteristic = {}
    weight = "0"

    for row in output.split('\n'):
        if re.match(r'.*weight', row):
            weight = row.split(" ")[1]
        elif re.match(r'\d*\s.*\s.*', row):
            var_name = row.split(" ")[2][1:-1]
            var_value = row.split(" ")[1]
            characteristic[var_name] = var_value

    return diffchars.DifferentialCharacteristic(characteristic, char_format,
                                                rounds, weight)


def getCharSTPOutput(output, char_format, rounds):
    """
    Parse the output of STP and construct a characteristic.
    """
    characteristic = {}
    weight = "0"
    for row in output.split('\n'):
        if re.match(r'ASSERT.*weight', row):
            weight = re.search(r'(?<=ASSERT\( weight = ).*(?= \);)', row).group(0)
        elif re.match(r'ASSERT\(.*\)', row):
            tmp = re.search(r'ASSERT\( ([a-z0-9A-Z]+) = ([a-z0-9A-Z]+)', row)
            var_name = tmp.group(1)
            var_value = tmp.group(2)
            characteristic[var_name] = var_value

    return diffchars.DifferentialCharacteristic(characteristic, char_format,
                                                rounds, weight)