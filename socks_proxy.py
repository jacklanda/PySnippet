#! /bin/python3.9
# Author: Jacklanda

# pip install PySocks
import socks

import socket


class ProxyOnSocket(object):
    """
    A temporary implementation of httpx socks5 proxy
    (on the base of Python Third Party Package: httpx, socks)

    Parameters:
    host - proxy host - default: localhost
    port - proxy port - default: 8888
    """

    def __init__(self, host: str = "127.0.0.1", port: str = 8888):
        socks.set_default_proxy(socks.SOCKS5, host, port)
        socket.socket = socks.socksocket

    def _proxy_test(self, url: str):
        import httpx
        with httpx.Client() as client:
            try:
                r = client.get(url)
                if(r.status_code == 200):
                    # print(r.content.decode())
                    print(
                        f"StatusCode: {r.status_code} -> Connect Success On SOCKS5 Proxy!")
                else:
                    print(
                        f"StatusCode: {r.status_code} -> SOCKS5 Connection Error!")
            except Exception as e:
                print(e)


if __name__ == "__main__":

    # pip install httpx
    import httpx

    # simple test for httpx socks5 proxy
    url = "https://zh.wikipedia.org/wiki/Python"
    ProxyOnSocket(port=1088)._proxy_test(url)
