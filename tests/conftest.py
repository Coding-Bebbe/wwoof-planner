"""Shared test setup. pytest loads this file automatically before the tests.

Rule (03_programmierprojekt.md, section 5.5): tests never access the network.
The fixture below enforces this for every test: any attempt to look up or
connect to a host other than this computer fails at once.
"""

import socket

import pytest

# Addresses of this computer. asyncio uses a local socket internally on
# Windows (needed by Playwright in step 2.2), so these stay allowed.
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


class NetworkAccessInTest(RuntimeError):
    """A test tried to reach the network.

    Deliberately not an OSError: code under test catches OSError for real
    network problems and would otherwise treat this as an ordinary failure.
    """


def _host_of(address) -> str:
    # connect() gets a tuple (host, port, ...); getaddrinfo() gets the host.
    host = address[0] if isinstance(address, tuple) else address
    if isinstance(host, bytes):
        host = host.decode("ascii", "replace")
    return str(host)


@pytest.fixture(autouse=True)  # autouse: applies to every test without being requested
def no_network(monkeypatch):
    original_getaddrinfo = socket.getaddrinfo
    original_connect = socket.socket.connect

    def guarded_getaddrinfo(host, *args, **kwargs):
        if _host_of(host) not in LOOPBACK_HOSTS:
            raise NetworkAccessInTest(f"Tests must not access the network (lookup of {host})")
        return original_getaddrinfo(host, *args, **kwargs)

    def guarded_connect(sock, address):
        if _host_of(address) not in LOOPBACK_HOSTS:
            raise NetworkAccessInTest(f"Tests must not access the network (connect to {address})")
        return original_connect(sock, address)

    # monkeypatch replaces the functions for the duration of one test
    # and restores the originals afterwards.
    monkeypatch.setattr(socket, "getaddrinfo", guarded_getaddrinfo)
    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
