import uuid
from threading import Thread
import copy
import logging
from datetime import datetime
import time
from math import sin
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


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


# method to be exposed through server

def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# method to be exposed through server
# uses a decorator to automatically convert to and from variants

@uamethod
def func(parent, value):
    return value * 2

def tree_up(path1):
        tags = converter.get_file(path1)
        myobj1 = server.get_objects_node()
        if tags != False:
            myvar2 = []
            for tags1 in tags:
                if tags1['value_float'] != '':
                    myvar2.append(
                        myobj1.add_variable(2, tags1['tag'], float(tags1['value_float']), ua.VariantType.Float))
                else:
                    myvar2.append(myobj1.add_variable(2, tags1['tag'], int(tags1['value_int']), ua.VariantType.Int64))
            for index in myvar2:
                index.set_writable()

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
               self.var.set_value(1)
            else:
               flag = 0
               self.var.set_value(0)
            tags = converter.get_file(path)
            if tags != False:
                if 'myvar2' in locals ():
                    for i in range(len(tags)):
                        if tags[i]['value_float'] != '':
                           myvar2[i].set_value(tags[i]['value_float'])
                        else:
                           myvar2[i].set_value(tags[i]['value_int'])
                else:
                    myvar2 = []
                    for tags1 in tags:
                        if tags1['value_float'] != '':
                            myvar2.append(myobj.add_variable(idx, tags1['tag'], float(tags1['value_float']),
                                                             ua.VariantType.Float))
                        else:
                            myvar2.append(myobj.add_variable(idx, tags1['tag'], float(tags1['value_int']), ua.VariantType.Int64))
                    for index in myvar2:
                        index.set_writable()

            print('In the work...')
            time.sleep(5)


if __name__ == '__main__':
    config = converter.get_config()
    path = config['path']
    time_period = config['UPDATE_RATE']

    # logging.basicConfig(level=logging.DEBUG)
    server = Server()

    server.set_endpoint(config['UA_HOST'])
    server.set_server_name(config['UA_SERVER_NAME'])
    # setup our own namespace, not really necessary but should as spec
    uri = config['UA_ROOT_NAMESPACE']
    idx = server.register_namespace(uri)
    # create a new node type we can instantiate in our address space
    dev = server.nodes.base_object_type.add_object_type(idx, "MyDevice")
    dev.add_variable(idx, "sensor1", 1.0)
    dev.add_property(idx, "device_id", "0340")
    ctrl = dev.add_object(idx, "controller")
    ctrl.set_modelling_rule(True)
    ctrl.add_property(idx, "state", "Idle").set_modelling_rule(True)
    myfolder = server.nodes.objects.add_folder(idx, "myEmptyFolder")
    # instanciate one instance of our device
    mydevice = server.nodes.objects.add_object(idx, "Device0001", dev)
    mydevice_var = mydevice.get_child(
        ["{}:controller".format(idx), "{}:state".format(idx)])  # get proxy to our device state variable
    # create directly some objects and variables
    myobj = server.nodes.objects.add_object(idx, "DATA")

    mysin = myobj.add_variable(idx, "Life_Server", 0, ua.VariantType.Float)




   # tree_up(path)



    # creating a default event object
    # The event object automatically will have members for all events properties
    # you probably want to create a custom event type, see other examples
    myevgen = server.get_event_generator()
    myevgen.event.Severity = 300

    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    vup = VarUpdater(mysin)  # just  a stupide class update a variable
    vup.start()
