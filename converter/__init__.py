
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

def last_file(directory):
    files = [os.path.join(directory, _) for _ in os.listdir(directory) if _.endswith('.txt')]
    if len(files)>0:
        return max(files, key=os.path.getctime)
    else:
        return False

def get_file(dir):
    res = []
    fl = last_file(dir)
    if fl != False:
        for line in open(fl, 'r'):
                 line = line.strip()
                 res.append(dict(zip(("tag", "date", "value_float", "value_int"), line.split(","))))
        return res
    else:
        return False


