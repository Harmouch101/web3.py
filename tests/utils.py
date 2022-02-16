import asyncio
import socket
import time
import warnings

import websockets


def get_open_port():
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return str(port)


async def wait_for_ws(endpoint_uri, timeout=10, event_loop=None):
    if event_loop is not None:
        warnings.warn(
            "The event_loop parameter is deprecated and was removed "
            "from websocket provider as of web3 v6. Consider calling "
            "this method without passing this argument instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
    start = time.time()
    stop = start + timeout
    while time.time() < stop:
        try:
            async with websockets.connect(uri=endpoint_uri):
                pass
        except (ConnectionRefusedError, OSError):
            await asyncio.sleep(0.01)
        else:
            break
