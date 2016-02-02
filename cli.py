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
import argparse
import pprint
import sys
import os
import hashlib

from libs import constants
from libs.connection import BuildCommand
from libs.connection import Connection
from libs.connection import Login
from libs.connection import SendPassword
from libs.cryptolib import decrypt_file_to_array
from libs.getpass import getpass
from libs.utils import BuildLogfile
from libs.utils import CleanComments


p = argparse.ArgumentParser(
   usage='''
   %(prog)s -r "remote host"| -f "list of hosts" [options]
   %(prog)s -h #get help on numerous options
   ''' % { "prog": sys.argv[0]},
   description='''
      A small tool to log into any piece of equipment with a decent CLI interface... 
      \nYou can pass a lot of options to comply with most of devices behavior.
      \n\n
      Note that if you ask %(prog)s to look for options in a file, that is "-o" option, 
      this file obviously contains your credentials, passwords,
      and thus MUST be encrypted using the "cipher.py" tool. 
            
      \n\nEnjoy ! 
   ''' % { "prog": sys.argv[0]},
   conflict_handler='resolve'
)

mut_excl_1 = p.add_mutually_exclusive_group()
mut_excl_1.add_argument('-f', '--hosts-file', action='store', type=str, dest='array', metavar='FILE', help='file containing a list of hosts')
mut_excl_1.add_argument('-r', '--remote-host', action='store', type=str, dest='remote', metavar='REMOTE_HOSTNAME', help='remote host name or IP')

mut_excl_2 = p.add_mutually_exclusive_group()
mut_excl_2.add_argument('-c', '--command', action='store',type=str, dest='cmd', nargs='+', metavar='COMMAND', 
    help='command(s) to be executed on remote host')
mut_excl_2.add_argument('-cf', '--command-file', action='store',type=str, dest='cmdfile', metavar='COMMAND_FILE',
    help='file containing a list of commands')

p.add_argument('-d', '--debug', action='store_true',dest='debug', help='debug mode will out in clear all arguments passed to the script')
p.add_argument('-i', '--interact', action='store_false',dest='interact', help='do not interact after connection')
p.add_argument('-j', '--jumphost-credentials', action='store',type=str, dest='jumphost', metavar='LIST', nargs='+',
    help='an ordered list: (protocol,host,port,username,password,prompt,timeout,verbose)\nyou can omit latest elements')
p.add_argument('-l', '--logfile', action='store_true', dest='logfile', help='create a logging file in "logs" subdirectory')
p.add_argument('-m', '--no-more', action='store',type=str, dest='more',
    help='command to pass to remote host to avoid --more-- in execution, defaults to "terminal length 0"')
p.add_argument('-o', '--options-override', action='store',type=str, dest='override', 
    help='ciphered file containing arguments that override command line options')
p.add_argument('-p', '--prompt', action='store',type=str, dest='prompt', help='expected prompt from remote host')
p.add_argument('-po', '--port-number', action='store',type=str, dest='port', metavar='TCP_PORT_NUMBER', help='TCP port number for connection')
p.add_argument('-s', '--sub-proc', action='store',type=str, dest='sub', nargs=2, metavar=('MODULE','METHOD'),
    help='module and function to execute')
p.add_argument('-t', '--timeout', action='store',type=int, dest='timeout', help='max seconds to wait for an answer from remote host')
p.add_argument('-u', '--username-credentials', action='store',type=str, dest='user', metavar=('USERNAME'),
    help='username to log into remote host')
p.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='unhide connection process, usefull for debugging')
p.add_argument('-w', '--password', action='store',type=str, dest='password', nargs='+', metavar=('PASSWORD'),
    help='password to log into remote host and optionally an enable password')
p.add_argument('-x', '--protocol', action='store',type=str, dest='proto', choices=['telnet','ssh'], 
    help='protocol to be used for connection, defaults to ssh')

p.set_defaults(          
   debug=False,
   interact=True,
   logfile=False,
   more='terminal length 0',
   prompt='\n[^\n]+[>#](\s|)$',
   proto='ssh',
   timeout='15',
   user='',
   verbose=False
)

# parse arguments from command line
args = p.parse_args()

# if "o" options is set,override arguments from local encrypted file 
if args.override:
   if not os.path.isfile(args.override):exit('ERROR: Invalid filename: "'+args.override+'"')
   else:
       password = getpass('Please enter your password: ')
       key = hashlib.sha256(password).digest()
       try:args_override = decrypt_file_to_array(key,args.override)
       except ValueError:exit('ERROR: The file '+args.override+' does not seem to be encrypted...')
       args_override_cleaned = CleanComments(args_override)
       if len(args_override_cleaned) == 0:
           exit('ERROR: wrong password, or file was empty...')
       #and now merge arguments in initial namespace
       else:p.parse_args(args_override_cleaned, namespace=args)

#if debug mode is on, we start with araw output of args
if args.debug:
    print('debug mode is on')
    pprint.pprint(vars(args))
    
# we need at least one of them
if (args.remote is None and args.array is None):
    p.error('ERROR: remote host IP address or name is required,\nyou miss either "-r" or "-f" option\n\n')

# here below, we try to get a host list from user arguments so we can iterate over this afterwards
if args.remote:
    listhosts_cleaned = [args.remote]
elif args.array:
    try:
       f = open(args.array)
       listhosts = f.read().splitlines()
       listhosts_cleaned = CleanComments(listhosts)
       args.interact = False
    except ValueError:
       print("ERROR: cannot open "+args.array+" not a usable file..")  
if args.debug:
    print('List of hosts:')
    pprint.pprint(listhosts_cleaned)

# if cmdfile or commands are provided, we build a list and sanitize it
if args.cmdfile:
    try:
        f = open(args.cmdfile)
        listcmd = f.read().splitlines()
        listcmd_cleaned = CleanComments(listcmd)
        args.interact = False
    except ValueError:
       print("ERROR: cannot open "+args.cmdfile+" not a usable file..")
elif args.cmd:
    listcmd_cleaned = CleanComments(args.cmd)
    args.interact = False
if args.debug and (args.cmdfile or args.cmd):
    print('List of commands:')
    pprint.pprint(listcmd_cleaned)   
    
# empty default port number if telnet without port options
if args.proto == 'telnet' and not args.port:args.port = ''
# defaults to port number 22 if ssh without port options
if args.proto == 'ssh' and not args.port:args.port = '22'

# complete password array with empty strings
if args.password:
    password = args.password[0]
    try:enablepassword = args.password[1]
    except:args.password.append('')

# complete jumphost credentials array with empty strings and initiate connection
if args.jumphost:
    try:args.jumphost[1]
    except:args.jumphost.append('ssh')
    try:args.jumphost[2]
    except:
        if args.jumphost[1] == 'ssh':args.jumphost.append('22')
        elif args.jumphost[1] == 'telnet':args.jumphost.append('')
    try:args.jumphost[3]
    except:args.jumphost.append('')
    try:args.jumphost[4]
    except:args.jumphost.append('')
    try:args.jumphost[5]
    except:args.jumphost.append('')
    c = Connection(*(args.jumphost+[args.timeout]+[args.verbose]))
    if c == False:exit('ERROR: Cannot connect to jumphost') 
    
#import sub procedure
if args.sub:
    import importlib
    try:
        mod = importlib.import_module(args.sub[0])
        submethod = getattr(mod, args.sub[1])  
    except ImportError as e:exit(e)

# main loop through hosts
for host in listhosts_cleaned:
    h = host.rstrip('\n')
    if not args.jumphost:
        c = Connection(
            args.proto,h,args.port,args.user,password,
            args.prompt,args.timeout,args.verbose
        )
        if c == False:
            print('ERROR: Cannot connect to remote host: '+h)
            continue
    else:
        cmd = BuildCommand(args.proto,h,args.port,args.user)
        c.sendline(cmd)
        l = Login(c,args.proto,h,args.port,args.user,password,
            args.prompt,args.timeout,args.verbose
        )
        if l == False:
            print('ERROR: Cannot connect to remote host: '+h)
            continue
    
    #now switch to enable mode if needed       
    if len(args.password[1]) > 0:
        c.sendline('enable')
        c.expect('assword:')
        if SendPassword(enablepassword,args.prompt,c,args.timeout):
            print("\n>>> connected to: "+h)
    
    #create a random name for logfile if asked to do so
    if args.logfile:
        logfile = BuildLogfile(h) 
        try:
           fout = open(logfile,'wb')
           # special case for commands logging
           if not (args.cmdfile or args.cmd):c.logfile_read = fout
           print("\t>>> now logging output from "+h+" in "+logfile)
        except (IOError, OSError) as e:
           print('cannot log output because logfile cannot be opened...')
           print "I/O error({0}): {1}".format(e.errno, e.strerror)
    else:c.logfile_read = sys.stdout

    # if commands in args or in a cmdfile, prepare terminal length
    if args.cmdfile or args.cmd:
        c.sendline(args.more)
        c.expect(args.prompt)
        print("\t>>> now executing commands from "+str(listcmd_cleaned)+" on "+h)
        # loop through the commands
        for line in listcmd_cleaned:
            c.sendline(line)
            c.expect(args.prompt)
            # if logfile is set, we send a clean output inside the loop
            if args.logfile:
               try:fout.write(c.before)
               except (IOError, OSError):print('WARNING: cannot log output to '+args.logfile)
        # and restore initial logging setup
        if args.logfile:c.logfile_read = fout
        else:c.logfile_read = sys.stdout
            
    #execute sub method
    if args.sub:
        try:submethod(c,args.prompt)
        except (ImportError,AttributeError,NameError) as e:exit(e)
    
    # pass in interact mode, hit ^F to end connection
    if args.interact is True:
        c.sendline('\n')
        c.expect(args.prompt)
        c.interact('\x06')
        print('\n<<< gracefully exited from: '+h+'\n')
    else:
        if not args.jumphost:c.close(force=True)
        else:
            c.sendline('exit')
            c.sendline()
            c.expect(args.jumphost[5])
        print('\n<<< gracefully exited from: '+h+'\n')