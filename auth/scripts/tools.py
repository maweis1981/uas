#!/usr/bin/env python
# encoding: utf-8
"""
tools.py

Created by Peter Ma on 2012-03-20.
Copyright (c) 2012 Maven Studio. All rights reserved.
"""

import sys
import os

import hashlib

def sign_request():
    from hashlib import sha1
    import hmac
    import binascii

    # If you dont have a token yet, the key should be only "CONSUMER_SECRET&"
    key = "tt contact" 

    # The Base String as specified here: 
    raw = "snda_uniform_user_profile" # as specified by oauth

    hashed = hmac.new(key, raw, sha1)

    # The signature
    return binascii.b2a_base64(hashed.digest())[:-1]

def main():
	consumer_key = 'NYqIbv9vCijVb2B6x7jhHg'
	print len(consumer_key)
	consumer_secret = 'fwqThazPj8UGUoEHgErQWjrePssvEdnYpHFuYLfL7jw'
	print len(consumer_secret)
	m = hashlib.md5()
	m.update('client app')
	print m.hexdigest()
	print len('0f9fab82e09dffaff1fd0ce80f63298e')
	print sign_request()
	print sign_request()
	print len(sign_request())


if __name__ == '__main__':
	main()

