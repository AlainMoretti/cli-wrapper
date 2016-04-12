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

#
# typical command line to launch this procedure would be : 
# cli.py -f hosts/routers -o profiles/myloginandpassword.enc -s subs.remove_ntp_server remove_ntp_server
#
# The expected result is :
# - connect to each router of "routers"
# - see if there are any ntp servers configured and remve them from the configuration
#
#we can perform any conditional action inside this block of code
def remove_ntp_server(args,c):
    #check if the router has some NTP servers configured
    c.sendline('show run ntp')
    c.expect(args.prompt)
    #grab and parse the output
    out = c.before
    outlist = out.split("\n")
    #go to configuration mode
    c.sendline('configure')
    c.expect(args.prompt)
    c.sendline('ntp')
    c.expect(args.prompt)
    for line in outlist:
        if line[0:7] == ' server':
            #now iterate over any configured ntp server and remove it from the config
            c.sendline("no "+c)
            c.expect(args.prompt)
    c.sendline('commit')
    c.expect(args.prompt)
    c.sendline('end')
    c.expect(args.prompt) 

def main():
    print "\n\n>>>>> this module is used as a parameter of main program, it does nothing by itself <<<<<<<<<\n\n"

if __name__ == "__main__":
    main()