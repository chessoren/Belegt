"""Sovereignty, demonstrated rather than claimed.

* ``audit``: a Python audit hook records every socket connection this process
  attempts. Anything that is not loopback is counted as an *outbound* attempt
  and blocked. The counter is shown in the UI and written into every receipt.
* ``state``: a *passive* look at the machine's network (interfaces and the
  routing table). No packet is sent to find out whether we are offline.
"""
from __future__ import annotations

import ipaddress
import os
import sys
import threading
from pathlib import Path

_lock = threading.Lock()
_outbound: list[str] = []
_loopback_calls = 0


def _is_loopback(host) -> bool:
    if host in ("localhost", "", None):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _hook(event, args):
    global _loopback_calls
    if event == "socket.connect":
        addr = args[1]
        host = addr[0] if isinstance(addr, tuple) else addr
        if isinstance(addr, str):  # unix socket
            return
        if _is_loopback(host):
            with _lock:
                _loopback_calls += 1
            return
        with _lock:
            _outbound.append(str(addr))
        raise PermissionError(f"Belegt blocks outbound connection to {addr}")
    if event == "socket.getaddrinfo":
        host = args[0]
        if isinstance(host, bytes):
            host = host.decode()
        if not _is_loopback(host):
            with _lock:
                _outbound.append(f"dns:{host}")
            raise PermissionError(f"Belegt blocks DNS lookup of {host}")


def install():
    sys.addaudithook(_hook)


def counters() -> dict:
    with _lock:
        return {"outbound_attempts": len(_outbound), "blocked": list(_outbound[-5:]),
                "loopback_calls": _loopback_calls}


def state() -> dict:
    ifaces = []
    base = Path("/sys/class/net")
    if base.exists():
        for d in sorted(base.iterdir()):
            if d.name == "lo":
                continue
            try:
                oper = (d / "operstate").read_text().strip()
            except OSError:
                oper = "unknown"
            ifaces.append({"name": d.name, "state": oper})
    default_route = False
    try:
        for line in Path("/proc/net/route").read_text().splitlines()[1:]:
            parts = line.split()
            if len(parts) > 2 and parts[1] == "00000000":
                default_route = True
    except OSError:
        pass
    try:
        for line in Path("/proc/net/ipv6_route").read_text().splitlines():
            parts = line.split()
            if parts and parts[0] == "0" * 32 and parts[1] == "00" and parts[-1] != "lo":
                default_route = True
    except OSError:
        pass
    up = [i for i in ifaces if i["state"] in ("up", "unknown")]
    offline = (not default_route) or (not up)
    return {"offline": offline, "default_route": default_route, "interfaces": ifaces,
            "pid": os.getpid(), **counters()}
