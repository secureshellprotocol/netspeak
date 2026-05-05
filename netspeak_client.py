import asyncio

import netspeak_config as config

async def get_user_input():
    # Runs the blocking input() in a separate thread to keep the loop free
    return await asyncio.to_thread(input, "Enter message: ")

async def tcp_interactive_client():
    try:
        reader, writer = await asyncio.open_connection(config.IP, config.PORT)
        print("Connected to netspeak server")

        while True:
            # Wait for an input and then shove it down the line
            message = await get_user_input()

            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(1024)
            if not data:
                print("Server closed the connection.")
                break

            print(f'Server echoed: {data.decode()!r}')

        print('Closing the connection...')
        writer.close()
        await writer.wait_closed()

    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Is it running?")

if __name__ == "__main__":
    try:
        asyncio.run(tcp_interactive_client())
    except KeyboardInterrupt:
        pass # Handle Ctrl+C gracefully
