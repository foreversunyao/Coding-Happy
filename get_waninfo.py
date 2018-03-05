#!/bin/python2.7
"""
get wan info from linux 

"""
import subprocess
#p =  subprocess.Popen(['ip route get 8.8.8.8'], shell =  True)
#print p.returncode

p =  subprocess.Popen(['ip route get 8.8.8.8'], shell =  True, stdout=subprocess.PIPE)
if p.returncode != 0:
	firstline = (p.communicate()[0]).split('\n', 1)[0]
	dev = firstline.split(' ')[4]
	gw = firstline.split(' ')[2]
	source = firstline.split(' ')[7]
	print "dev: " + dev
	print "gw: " + gw
	print "source: " + source


