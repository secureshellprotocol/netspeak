import asyncio
import pyttsx3
import queue
import threading

import netspeak_config as config

class TTSEngine:
    engine=None

    def __init__(self):
        self.engine = pyttsx3.init()

    def start(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

say_queue = queue.Queue()

def worker():
    tts = TTSEngine()
    while True:
        phrase = say_queue.get()
        tts.start(phrase)
        say_queue.task_done()

threading.Thread(target=worker, daemon=True).start()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            break

        message = data.decode()
        print(f"Speaking {message!r} from {addr}...", end='', flush=True)

        say_queue.put(message)

        print(f'done')
        writer.write(data)
        await writer.drain()  # Ensure the data is sent

    print(f"Closing connection with {addr}")
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, config.IP, config.PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
