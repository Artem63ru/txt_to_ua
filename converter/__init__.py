
import xml.etree.ElementTree as ET
import os
import os.path

def get_config(configFile='cfg.xml'):
    tree = ET.parse(configFile)
    root = tree.getroot()
    res = {}
    for child in root:
        res[child.tag] = child.text

    return res

def get_file(dir):
    n = 0
    res = []
    for file in os.listdir(dir):
            if file.endswith(".txt"):
             fl = os.path.join(dir, file)
             for line in open(fl, 'r'):
                 line = line.strip()
                 res.append(dict(zip(("tag", "date", "value_float", "value_int"), line.split(","))))
             file_new = ''.join((file, '_'))
             os.rename(file, file_new)
             return res
    return False


