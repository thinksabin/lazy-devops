#!/usr/bin/python
__author__ = 'thinksabin'

#Execute the script with the following command:
#    fab -i /location/to/ssh/key--port 22 -H frog@subisu.lftechnology.com create

from fabric.api import *


# Editable Config
local_user = "sabin" # local user of the workstation from which this fabfile is run
ssh_user = "ubuntu" # username used to ssh to the remote machine
key_dir = "/home/sabin/keys/" # the location where the keys are to be copied in the local workstation


def create():
    choice = ""
    while choice != ("N" or "n" or "No"):
        print "\n\n-------------  Creating user on %s  -------------\n"
        username = prompt("Enter Username to create:")
        
        print username
        try:
            sudo("adduser %s" %username)
            print "\n------------- User created  -------------\n"
        except:
            print "\n------------- User already exists  -------------\n"
            pass
        print "\n------------- Creating Keys -------------\n"
        with cd("/home/%s" %username):
            sudo("ssh-keygen -b 1024 -f %s -t dsa" %username)
            try:
                sudo("mkdir .ssh")
            except:
                pass
            print "\n------------- Keys created  -------------\n"
            sudo("chmod 700 .ssh")
            sudo("cat %s.pub >> .ssh/authorized_keys" %username)
            sudo("mv %s %s.pem" %(username,username) )
            sudo("chmod 600 .ssh/authorized_keys")
            sudo("chown %s .ssh" %username)
            sudo("chown %s .ssh/authorized_keys" %username)
            sudo("chmod 600 %s.pem" %username)
            sudo("chown %s:%s /home/%s -R" %(username,username,username))
            try:
                sudo("mkdir /home/Keys")
                sudo("mv %s.pem /home/Keys" %username)
                sudo("mv %s.pub /home/Keys" %username)
            except:
                sudo("mv %s.pem /home/Keys" %username)
                sudo("mv %s.pub /home/Keys" %username)
            sudo("chown %s /home/Keys -R" %ssh_user)
            make_sudo = prompt("Do you want to provide Sudo right to %s ? (Y/N)" %username)
            if make_sudo == "Y" or make_sudo == "y" or make_sudo == "yes":
                try:
                    print(" Giving Sudo Access to username: %s" %username)
                    sudo("sed '/#\ User\ privilege\ specification/a\%s\    ALL=(ALL:ALL)\ NOPASSWD:ALL' /etc/sudoers --in-place" %username)
                except:
                    print(" Couldnt Grant Sudo Access to %s" %username)
                    pass
            else:
                print("No access given to %s" %username)
        print "\n------------- Downloading Keys -------------\n"
        get("/home/Keys/%s.*" %username,"/tmp")

        local("chown %s /tmp/%s.* " %(local_user,username))
        local("mv /tmp/%s.* %s" %(username,key_dir))
        print "\n\n------------- Key files downloaded to %s   -------------\n" %key_dir

        choice = prompt("Do you want to create another user (Y/N):")
    print "\n------------- Thank you  -------------\n"
