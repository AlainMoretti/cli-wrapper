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



#some constants used in the application
#you can change any of them to fit your needs without breaking anything !!!
DEFAULT_PROTOCOL='ssh'
DEFAULT_SHELL='/bin/bash'

#here below you can define what is the escape character in interaction mode
#defaults to 'Ctrl - ]' which is the common escape char in telnet
#if you want a 'Ctrl - C' instead, the code is '\x03'
ESCAPE_CHARACTER='\x1d'

LOGDIR = 'logs'

# LOGFILE_NAME can be: 
# CODE            EXAMPLE  
# RANDOM_STRING   remote-host_BDB0148E53E6.log
# DATE            remote-host_20160130145907.log
LOGFILE_NAME='RANDOM_STRING' 

LOGFILE_EXTENSION='.txt'

#here below the default command that will be sent to avoid the '--more--' prompt
MORE='terminal length 0'
#'none' is a special value that avoids sending even a <CR>
# MORE='none' 

#The prmopt here below also matches ANSI colored prompts: 
PROMPT='(\x1b\[[^m]*m|)[\w\d\-_]+[>#]'
#If you are sure that you don't need to match colored prompts, you could use this simpler one : 
#PROMPT='\n[^\n]+[>#](\s|)$'


PASSWORD_PROMPT='(p|P)assword:\s?$'

# here below you can pass arguments to ssh except '-p' and '-l'
# that are already used by the application itself
# SSH_BINARY = '/usr/bin/ssh'
SSH_BINARY = 'ssh'

# here after you can define the SSH command form that you will use
# valid options are :  
#    'USER_AT_HOST' eg : ssh username@hostname
#    'L_OPTION'     eg : ssh -l username hostname
SSH_COMMAND = 'USER_AT_HOST'

# you can change name or path to telnet executable
TELNET_BINARY = 'telnet'

# you can customize the command used to exit an interactive session to a host
EXIT_COMMAND = 'exit'