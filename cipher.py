#!/usr/bin/env python

# Copyright 2016 Netfishers
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import os.path
import re

from libs import constants
from libs.getpass import getpass
from libs.cryptolib import encrypt_file
from libs.cryptolib import decrypt_file


askedaction = raw_input('What do you wanna do ? decrypt/encrypt - [D/e]: ')
if (re.match('^(?i)d(ecrypt|)$',askedaction) or not askedaction): action = 'decrypt'
elif (re.match('^(?i)e(ncrypt|)$',askedaction)): action = 'encrypt'
else: exit('Invalid value: "'+askedaction+'"')

askedfile = raw_input('What is the filename you want to '+action+' ? ')
if os.path.isfile(askedfile):file = askedfile
else: exit('Invalid filename: "'+askedfile+'"')

password = getpass('Please enter your password: ')
key = hashlib.sha256(password).digest()

if action == 'encrypt':
    encrypt_file(key,file)
    print('Encrypt "'+file+'" and save it in "'+file+'.enc"')
elif action == 'decrypt':
    outfile = raw_input('Name of clear file to be created ? ')
    decrypt_file(key,file,outfile)
    print('Decrypt "'+file+'" and save it to "'+outfile+'"')