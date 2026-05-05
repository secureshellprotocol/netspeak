import asyncio

async def handle_client(reader, writer):
    """Callback function for every new connection."""
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")

    while True:
        # 1. Wait for data (non-blocking)
        data = await reader.read(1024)
        if not data:
            break

        message = data.decode()
        print(f"Received {message!r} from {addr}")

        # 2. Echo the data back
        writer.write(data)
        await writer.drain()  # Ensure the data is sent

    print(f"Closing connection with {addr}")
    writer.close()
    await writer.wait_closed()

async def main():
    # 3. Create and start the server event loop
    IP='10.69.0.2'
    PORT=42069
    server = await asyncio.start_server(handle_client, IP, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

# 4. Run the top-level entry point
if __name__ == "__main__":
    asyncio.run(main())
