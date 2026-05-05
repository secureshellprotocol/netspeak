import asyncio
import pyttsx3

engine=pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

async def handle_client(reader, writer):
    """Callback function for every new connection."""
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            break

        message = data.decode()
        print(f"Speaking {message!r} from {addr}...", end='')

        await asyncio.to_thread(speak, message)

        print(f'done')
        writer.write(data)
        await writer.drain()  # Ensure the data is sent

    print(f"Closing connection with {addr}")
    writer.close()
    await writer.wait_closed()

async def main():
    IP='10.69.0.2'
    PORT=42069
    server = await asyncio.start_server(handle_client, IP, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
