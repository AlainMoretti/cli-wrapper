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

def Connection(protocol,host,port,username,password,prompt,timeout,verbose):
    if protocol == 'ssh':
       cmd = 'ssh -p '+str(port)+' -l '+username+' '+host
    elif protocol == 'telnet':
       cmd = 'telnet '+host+' '+port
    p = pexpect.spawn('bash',['-c', cmd],timeout=timeout)
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
        '((u|U)sername|(l|L)ogin):',
        '(p|P)assword:',
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
        print('seems that we didn\'t send the right password')
        res = False
    elif index == 2:
        print('\ntimeout after '+str(timeout)+' seconds when trying to send password...')
        res = False
    elif index == 3:
        print('\nremote host unexpectedly closed the connection when sending password...')
        res = False
    return res

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