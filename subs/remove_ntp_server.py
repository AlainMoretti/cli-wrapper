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

def main():
    print "\n\n>>>>> now entering in a subprocess and execute some additional and custom commands <<<<<<<<<\n\n"

#
# typical command line to launch this procedure would be : 
# cli.py -f hosts/routers -o profiles/myloginandpassword.enc -s subs/remove_ntp_server remove_ntp_server
#
# The expected result is :
# - connect to each router of "routers"
# - see if there are any ntp servers configured and remve them from the configuration
#
#we can perform any conditional action inside this block of code
def remove_ntp_server(p,prompt):
    #check if the router has some nt servers configured
    p.sendline('show run ntp')
    p.expect(prompt)
    #grab and parse the output
    out = p.before
    outlist = out.split("\n")
    #go to configuration mode
    p.sendline('configure')
    p.expect(prompt)
    p.sendline('ntp')
    p.expect(prompt)
    for c in outlist:
        if c[0:7] == ' server':
            #now iterate over any configured ntp server and remove it from the config
            p.sendline("no "+c)
            p.expect(prompt)
    p.sendline('commit')
    p.expect(prompt)
    p.sendline('end')
    p.expect(prompt) 
        
if __name__ == "__main__":
    main()