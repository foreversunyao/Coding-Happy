#!/bin/python2.7
import requests
files = {'file': open('merge.txt')}

files2 = {'file': open('file.txt')}
files3 = {'file': open('1.txt')}

#url='http://10.10.52.164:8000/ttt/mmmm111'
#r = requests.post(url, files=files2)
#print r.text
#print r.status_code
#
url='http://10.10.52.164:8000/api/upload'
r = requests.post(url, files=files2)
print r.text
print r.status_code

url='http://10.10.52.164:8000/api/upload'
r = requests.post(url, files=files3)
print r.text
print r.status_code

url='http://10.10.52.164:8000/api/retrieve'
r = requests.post(url, files=files2)
print r.text
print r.status_code

url='http://10.10.52.164:8000/api/retrieve'
r = requests.post(url, files=files3)
print r.text
print r.status_code


url='http://10.10.52.164:8000/api/delete'
r = requests.post(url, files=files2)
print r.text
print r.status_code

url='http://10.10.52.164:8000/api/delete'
r = requests.post(url, files=files3)
print r.text
print r.status_code


url='http://10.10.52.164:8000/api/retrieve'
r = requests.post(url, files=files2)
print r.text
print r.status_code

url='http://10.10.52.164:8000/api/retrieve'
r = requests.post(url, files=files3)
print r.text
print r.status_code
