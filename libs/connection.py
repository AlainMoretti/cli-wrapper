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

import pexpect
import sys

from libs import constants


def BuildCommand(protocol,host,port,username):
    res = False
    if protocol == 'ssh':
       if username == '':exit("ERROR:: you cannot use ssh without a username...")
       cmd = constants.SSH_BINARY+' -p '+str(port)+' -l '+username+' '+host
       res = True
    elif protocol == 'telnet':
       cmd = constants.TELNET_BINARY+' '+host+' '+port
       res = True
    if res: return cmd
    else: return False

def CleanComments(array):
    cleaning = False
    for i, item in enumerate(array):
        if item[0] == '#':
            array[i] = ''
            cleaning = True
    array = [x.strip(' ') for x in array]
    remove = True
    while remove:
        try:
            array.remove('')
        except:remove = False
    return array

def Connection(protocol,host,port,username,password,prompt,timeout,verbose):
    try:cmd = BuildCommand(protocol, host, port, username)
    except ValueError as e:exit(e)
    
    p = pexpect.spawn(constants.DEFAULT_SHELL,['-c', cmd],timeout=timeout)
    if verbose is True:p.logfile_read = sys.stderr 
    if Login(p,protocol,host,port,username,password,prompt,timeout,verbose):
        return p
    else:
        return False

def Login(p,protocol,host,port,username,password,prompt,timeout,verbose):    
    res = False
    index = p.expect([
        prompt,
        "Are you sure you want to continue",
        '((u|U)sername|(l|L)ogin):\s?$',
        '(p|P)assword:\s?$',
        pexpect.TIMEOUT,
        pexpect.EOF
    ])
    if index == 0:
        res = True
    elif index == 1:
        p.sendline('yes')
        p.expect('assword:')
        if SendPassword(password,prompt,p,timeout):
           res = True       
    elif index == 2:
        if username == '':exit("ERROR: you haven't provided any username, but remote host is asking for it...")
        p.sendline(username)
        p.expect('assword:')
        if SendPassword(password,prompt,p,timeout):
           res = True 
    elif index == 3:
        if SendPassword(password,prompt,p,timeout):
           res = True 
    elif index ==4:
        print('\ntimeout after '+str(timeout)+' seconds when trying to '+protocol+' to '+host+':'+port)
        res = False
    elif index == 5:
        print('\n'+host+' unexpectedly closed the connection')
        res = False
    return res

def SendPassword(password,prompt,connection,timeout):
    res = False
    connection.sendline(password)
    index = connection.expect([
        prompt,
        '(p|P)assword:',
        pexpect.TIMEOUT,
        pexpect.EOF
    ])
    if index == 0:
        res = True
    elif index == 1:
        connection.sendline(password)
        print('ERROR: seems that we didn\'t send the right password')
        res = False
    elif index == 2:
        print('\ntimeout after '+str(timeout)+' seconds when trying to send password...')
        res = False
    elif index == 3:
        print('\nremote host unexpectedly closed the connection when sending password...')
        res = False
    return res