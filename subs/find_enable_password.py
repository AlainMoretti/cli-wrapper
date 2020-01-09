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


# the following method allows Cisco enable password discovery when scrolling through a list of devices. 
# it interacts with the actual connection, tries enable passwords from a list, 
# then prints out the hostname;password and finally returns control to the main loop 
# typical command line to launch this procedure would be :
# cli.py -f hosts/routers -o profiles/myloginandpassword.enc -s subs.find_enable_password find_enable_password
def find_enable_password(args,c):
    import pexpect
    c.sendline('!')
    index = c.expect([
        '>',
        '.*#',
        pexpect.EOF,
        pexpect.TIMEOUT
    ])
    need_enable = False
    already_enable = False
    if index == 0:
        need_enable = True
    elif index == 1:
        already_enable = True
    elif index == 2: print ("::"+args.remote+";ERROR\n")
    elif index == 3: print ("::"+args.remote+";TIMEOUT\n")
    if need_enable:
        password = 'UNKNOWN'
        got_enable = False
        passwords = ('password1','password2','password3')
        i = 0
        while got_enable is not True and i < 3:
            c.sendline('enable')
            enable_test = c.expect(['assword:',pexpect.TIMEOUT])
            if enable_test == 1:
               got_enable = True
               password = 'UNKNOWN'
               break
            c.sendline(passwords[i])
            result = c.expect([
                '>',
                '#'
            ])
            if result == 1:
               got_enable = True
               password = passwords[i]
            i += 1
        print ("::"+args.remote+";"+password+"\n")
    elif already_enable: print ("::"+args.remote+";NONE\n")


def main():
    print ("\n\n>>>>> this module is used as a parameter to the main program, it does nothing by itself <<<<<<<<<\n\n")

if __name__ == "__main__":
    main()