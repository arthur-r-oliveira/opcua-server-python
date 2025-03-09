import asyncio
from asyncua import Server, ua
import psycopg2

# PostgreSQL Configuration
DB_HOST = "ushift05.stormshift.coe.muc.redhat.com"
DB_PORT = "31713"
DB_USER = "ps_user"
DB_PASSWORD = "SecurePassword"
DB_NAME = "ps_db"

async def main():
    # OPC UA Server Setup
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    # Namespace and Objects
    uri = "http://example.com"
    idx = await server.register_namespace(uri)
    objects = server.nodes.objects

    # Sensor Values Folder
    sensor_folder = await objects.add_folder(idx, "SensorValues")

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME
        )
        cur = conn.cursor()
        print(f"Looks like that we've connected to Postgres")
        # Fetch Sensor Data
        cur.execute("SELECT sensor_id, value FROM sensor_values;")
        rows = cur.fetchall()

        # Create OPC UA Nodes
        for row in rows:
            sensor_id, value = row
            sensor_node = await sensor_folder.add_variable(
                idx, sensor_id, value, ua.VariantType.Double
            )
            await sensor_node.set_writable()

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return

    # Start the Server
    async with server:
        print("OPC UA server started...")
        await asyncio.Event().wait()  # Keep the server running

if __name__ == "__main__":
    asyncio.run(main())
