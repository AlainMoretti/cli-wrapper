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
MORE='terminal length 0'
PROMPT='\n[^\n]+[>#](\s|)$'
PASSWORD_PROMPT='(p|P)assword:\s?$'
PROTOCOL='ssh'
# here below you can pass arguments to ssh except '-p' and '-l'
# that are already used by the application itself
SSH_BINARY = '/usr/bin/ssh'
TELNET_BINARY = 'telnet'