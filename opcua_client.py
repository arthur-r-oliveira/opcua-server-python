import asyncio
from asyncua import Client

async def main():
    url = "opc.tcp://localhost:4840"  # Replace with your server URL if different

    async with Client(url=url) as client:
        uri = "http://example.com"
        idx = await client.get_namespace_index(uri)

        sensor_folder = await client.nodes.objects.get_child(
            ["2:SensorValues"]
        )  # 2 is the index of the "Objects" folder.

        children = await sensor_folder.get_children()

        for child in children:
            if await child.read_node_class() == 2: # Variable Node
                value = await child.read_value()
                node_name = await child.read_browse_name() # Corrected line
                print(f"{node_name.Name}: {value}")

if __name__ == "__main__":
    asyncio.run(main())
