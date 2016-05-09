#!env/bin/python

import boto3
import sys
import json
import time

if len(sys.argv) < 2:
	print "usage: {0} <function> [arguments]\nuse help for list command"
	sys.exit(1)

def init_session():
	s = boto3.Session(profile_name='ec2')
	return s.resource('ec2')

def ls():
	ec2 = init_session()
	for i in ec2.instances.all():
		print(i)

def help():
	print "list command:\nstart [instance_name]\nstop [instance_name]\nstate"

def stop():
	ec2 = init_session()
	if len(sys.argv) == 2:
		print "usage: {0} stop [instance_name]"
		sys.exit(1)

	instance_name = sys.argv[2]
	for i in ec2.instances.all():
		for x in i.tags:
			if (x['Key'] == 'Name') and (x['Value'] == instance_name):
				state = i.state['Name']
				if state == 'running':
					i.stop()
					print "waiting for instance to stop..."
					i.wait_until_stopped()
					print "instance:%s is stopped" % (instance_name)
					sys.exit(1)
				else:
					print 'instance_name:%s is stopped' % (instance_name)
					sys.exit(1)

	print 'instance_name not found'

def start():
	ec2 = init_session()
	if len(sys.argv) == 2:
		print "usage: {0} start [instance_name]"
		sys.exit(1)

	instance_name = sys.argv[2]
	for i in ec2.instances.all():
		for x in i.tags:
			if (x['Key'] == 'Name') and (x['Value'] == instance_name):
				state = i.state['Name']
				if state == 'stopped':
					i.start()
					print "waiting for instance to up..."
					i.wait_until_running()
					public_dns_name = i.public_dns_name
					public_ip_addr = i.public_ip_address
					print "instance:%s is up, you can connect to %s or %s" % (instance_name, public_dns_name, public_ip_addr)
					sys.exit(1)
				else:
					print 'instance_name:%s is running' % (instance_name)
					sys.exit(1)

	print 'instance_name not found'


def state():
	ec2 = init_session()
	for i in ec2.instances.all():
		state = i.state
		state = state['Name']
		tags = i.tags
		public_dns_name = i.public_dns_name
		public_ip_addr = i.public_ip_address
		private_ip_addr = i.private_ip_address
		instance_name = ''
		for x in tags:
			if(x['Key'] == 'Name'):
				instance_name = x['Value']

		print 'instance_name: %s state: %s public_dns_name: %s public_ip_address: %s private_ip_address: %s\n' % (instance_name, state, public_dns_name, public_ip_addr, private_ip_addr)

if __name__ == '__main__':
	getattr(sys.modules[__name__], sys.argv[1])()