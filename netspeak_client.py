import asyncio

async def get_user_input():
    # Runs the blocking input() in a separate thread to keep the loop free
    return await asyncio.to_thread(input, "Enter message (or 'quit' to exit): ")

async def tcp_interactive_client():
    IP = '10.69.0.2'
    try:
        reader, writer = await asyncio.open_connection('10.69.0.2', 42069)
        print("Connected to the server!")

        while True:
            # 1. Get input from user
            message = await get_user_input()

            if message.lower() in ['quit', 'exit']:
                break

            # 2. Send to server
            writer.write(message.encode())
            await writer.drain()

            # 3. Wait for echo
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
