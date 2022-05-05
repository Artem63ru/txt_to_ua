import logging
import asyncio
import sys
import converter

sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod



@uamethod
def func(parent, value):
    return value * 2



async def main():
    # _logger = logging.getLogger('asyncua')
    # setup our server
    config = converter.get_config()
    path = config['path']
    time_period = config['UPDATE_RATE']
    tags = converter.get_file(path)
    server = Server()
    await server.init()
    server.set_endpoint(config['UA_HOST'])
    server.set_server_name(config['UA_SERVER_NAME'])
    # setup our own namespace, not really necessary but should as spec
    uri = config['UA_ROOT_NAMESPACE']
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(2, 'MyObject')

    if tags != False:
        myvar = []
        for tags1 in tags:
            myvar.append(await myobj.add_variable(idx, tags1['tag'], tags1['value']))
        for index in myvar:
            await index.set_writable()
    # Set MyVariable to be writable by clients

    # await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func, [ua.VariantType.Int64], [ua.VariantType.Int64])
    # _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(int(time_period))
            tags = converter.get_file(path)
            if tags != False:
              if 'myvar' in locals():
                for i in range(len(tags)):
                  await myvar[i].write_value(tags[i]['value'])
              else:
                myvar = []
                for tags1 in tags:
                    myvar.append(await myobj.add_variable(idx, tags1['tag'], tags1['value']))
                for index in myvar:
                    await index.set_writable()
            # await myvar.write_value(0.5)
            print('In the work...')


if __name__ == '__main__':

    # logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main())