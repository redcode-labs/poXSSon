#!/usr/bin/python3.7
name="hide"
description="Hides specified element on the page"
options = [['ELEMENT_ID', "ID of the element to hide", ""]]

payload = """
var p = document.getElementById('ELEMENT_ID');
p.style.display = 'none';

"""
