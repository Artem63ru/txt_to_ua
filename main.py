import uuid
from threading import Thread
import copy
import logging
import datetime
import time
import sys
import converter


from opcua.ua import NodeId, NodeIdType

sys.path.insert(0, "..")

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()

from opcua import ua, uamethod, Server






class VarUpdater(Thread):
    def __init__(self, var):
        Thread.__init__(self)
        self._stopev = False
        self.var = var

    def stop(self):
        self._stopev = True

    def run(self):
        flag = 0
        while not self._stopev:

            if flag != 1:
               flag = 1
               self.var.set_value(True)
            else:
               flag = 0
               self.var.set_value(False)
            tags = converter.get_file(path)
            if tags != False:
                if 'myvar2' in locals():
                    for i in range(len(tags)):
                        if tags[i]['value_float'] != '':
                           timestamp = datetime.datetime.strptime(tags[i]['date'], '%d-%b-%Y %H:%M:%S')
                           datavalue = ua.DataValue(variant=tags[i]['value_float'], sourceTimestamp=timestamp)
                           myvar2[i].set_value(datavalue)
                        else:
                           timestamp = datetime.datetime.strptime(tags[i]['date'], '%d-%b-%Y %H:%M:%S')
                           datavalue = ua.DataValue(variant=tags[i]['value_int'], sourceTimestamp=timestamp)
                           myvar2[i].set_value(datavalue)
                else:
                    myvar2 = []
                    for tags1 in tags:
                        if tags1['value_float'] != '':
                            var = myobj.add_variable(idx, tags1['tag'], float(tags1['value_float']),
                                                     ua.VariantType.Float)
                            myvar2.append(var)
                            timestamp = datetime.datetime.strptime(tags1['date'], '%d-%b-%Y %H:%M:%S')
                            datavalue = ua.DataValue(variant=tags1['value_float'], sourceTimestamp=timestamp)
                            var.set_value(datavalue)
                        else:
                            var = myobj.add_variable(idx, tags1['tag'], float(tags1['value_int']),
                                                     ua.VariantType.Int64)
                            myvar2.append(var)
                            print('In the work..Int64.')
                            timestamp = datetime.datetime.strptime(tags1['date'], '%d-%b-%Y %H:%M:%S')
                            datavalue = ua.DataValue(variant=tags1['value_int'], sourceTimestamp=timestamp)
                            var.set_value(datavalue)

            print('In the work...')
            time.sleep(10)


if __name__ == '__main__':
    config = converter.get_config()
    path = config['path']
    time_period = config['UPDATE_RATE']

    server = Server()

    server.set_endpoint(config['UA_HOST'])
    server.set_server_name(config['UA_SERVER_NAME'])
    # setup our own namespace, not really necessary but should as spec
    uri = config['UA_ROOT_NAMESPACE']
    idx = server.register_namespace(uri)
    myobj = server.nodes.objects.add_object(idx, "DATA")

    date_time_str = '29-Sep-2021 12:27:43'
    timestamp = datetime.datetime.strptime(date_time_str, '%d-%b-%Y %H:%M:%S')
    datavalue = ua.DataValue(variant=True, sourceTimestamp=timestamp)

    mysin = myobj.add_variable(idx,"Life_Server", False, ua.VariantType.Boolean)
    # mysin = myobj.add_variable(idx, "Life_Server", 42)

    mysin.set_value(datavalue)


    # starting!
    server.start()
    vup = VarUpdater(mysin)  # just  a stupide class update a variable
    vup.start()
