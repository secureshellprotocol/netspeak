# Netspeak

TTS over TCP/IP, using python's asyncio library

## Usage

Pull the repo and enter the directory. In a terminal:

```
uv sync
source .venv/bin/activate
```

Set your server's IP / Port in `netspeak_config.py`.

To run the server:
```
python3 netspeak_server.py
```

To run the client:
```
python3 netspeak_client.py
```
