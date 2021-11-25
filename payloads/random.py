#!/usr/bin/python3
import random
name="random"
description="Chooses a random one-liner payload for blind testing backend's input validation"
options = [[]] 
payload = random.choice(open('random_payloads.txt').readlines())
