# check_huntress
A Nagios plugin to check the huntress API

~~~
chrios@MT-AUD8160HV9:~$ ./check_huntress.py -h
usage: check_huntress.py [-h] [-p PUBLICKEY] [-s SECRETKEY]

options:
  -h, --help            show this help message and exit
  -p PUBLICKEY, --publickey PUBLICKEY
                        Your Huntress API public key
  -s SECRETKEY, --secretkey SECRETKEY
                        Your Huntress API private key
~~~
## To use:
Clone this repo into /usr/local/src:
~~~
cd /usr/local/src
git clone https://github.com/chrios/check_huntress.git
~~~
Put the following into your /etc/nagios4/objects/commands.cfg file:
~~~
define command {
        command_name            check-huntress
        command_line            /usr/bin/python3 /usr/local/src/check_huntress/check_huntress.py $ARG1$
}
~~~
Go to your huntress portal, and generate an API key pair.

Create a host object to check huntress:
~~~
define host {
        parents         Internal Systems
        host_name       Huntress
        address         127.0.0.1
        max_check_attempts      3
        check_period            24x7
        contact_groups          admins
        notification_interval   24x7
        notification_period     workhours
        check_command           check-huntress! -p 'public_key_here' -s 'private_key_here'
}
~~~
Reload nagios and test it out.
