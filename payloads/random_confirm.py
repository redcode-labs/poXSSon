#!/usr/bin/python3
import random
name="random_confirm"
description="Chooses a random one-liner 'confirm()' payload. An alternative to standard 'alert()'"
options = [[]] 
payload = random.choice(open('random__confirm_payloads.txt').readlines())
