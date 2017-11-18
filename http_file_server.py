#!/bin/python2.7

"""Simple HTTP Server.

Support upload files
Support search files
Support delete files
Support compress files
"""

"""Limit.
Only implement Post request
"""

"""Usage.
For server:
mkdir -p /var/upload/compress/
chmod 600 /var/upload
python http_file_server.py

For client:
Upload:
import requests
files ={'file': open('abc.txt')}
url='http://ip:8000/api/upload'
r = requests.post(url, files=files)
print r.text
print r.status_code
"""

"""
Author:Samuel 
Date:20171118
"""

import os
import BaseHTTPServer
import urllib
import cgi
import sys
#import shutil
#import mimetypes
import time
import tarfile


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Serve a GET request."""
	## TO DO

    def return_POST(self,r,m):
	## REPONSE INFO
	info_code = {0: 'upload success',1: 'upload failed',2: 'exists file',3: 'no this file',4: 'delete success',5: 'merge success', 6: 'merge failed'}
        if r:
            self.send_response(200)
	    self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("<html><head><title>Response.</title></head>")
            self.wfile.write("<body><p>OK</p>")
            self.wfile.write("<p>%s</p>" % info_code[m])
            self.wfile.write("</body></html>")
            self.wfile.close()
        else:
	    self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("<html><head><title>Response.</title></head>")
            self.wfile.write("<body><p>Error</p>")
            self.wfile.write("<p>%s</p>" % info_code[m])
            self.wfile.write("</body></html>")
            self.wfile.close()

    def do_POST(self):
        """Serve a POST request."""
	form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type'],
                             })
	upload_path="/var/upload"

	if "/api/upload" in self.path:
		self.upload_file(form,upload_path)
	elif "/api/search" in self.path:
		self.search_file(form,upload_path)
                self.do_GET()
	elif "/api/delete" in self.path:
		self.delete_file(form,upload_path)
                self.do_GET()
	elif "/api/merge" in self.path:
		self.merge_file(form,upload_path)
                self.do_GET()
	else :
		self.do_GET()

    def merge_file(self,form,upload_path):
	
	filenameList = form['file'].value
        timestamp = int(time.time())
	compression_path=upload_path+'/compress'
        targettarfilename = "compression-" + str(timestamp) + ".tar.gz"
	if not os.path.exists(compression_path):
                os.makedirs(compression_path)
        filepath = os.path.join(compression_path, targettarfilename)
	tar = tarfile.open(filepath,"w:gz")
	## IF FILENAME IN FILENAMELIST DOES NOT EXIST IN THE PATH
        flag = 0
	os.chdir(upload_path)
	for filename in filenameList.split():
		subfilepath = os.path.join(upload_path, filename)
		if os.path.exists(subfilepath):
			tar.add(filename)
		## IF FILE DOSE NOT EXIST IN THE PATH
		else :
			flag = 1
			break
	tar.close()
	##IF ONE FILE DOSE NOT EXIST IN THE PATH
	if flag == 1 :
		if os.path.exists(filepath):
			os.remove(filepath)
		self.return_POST(0,6)
	else :
		filepath = os.path.join(compression_path, "compressionfile.list")
        	f = open(filepath, 'a+')
		f.write(targettarfilename)
		f.write('\n')
		for filename in filenameList.split():
			subfilepath = os.path.join(upload_path, filename)
                	if os.path.exists(subfilepath):
				f.write(subfilepath)
				f.write('\n')
				os.remove(subfilepath)
        	self.return_POST(1,5)


    def upload_file(self,form,upload_path):
	
	filename = form['file'].filename
        filepath = os.path.join(upload_path, filename)
        compressionfile_path=upload_path+'/compress/compressionfile.list' 
	if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
	if os.path.exists(filepath):
		    self.return_POST(1,2)
	## FOR SAME FILENAME IN COMPRESSED FILES
	elif os.path.exists(compressionfile_path) and filename in open(compressionfile_path).read():
		    self.return_POST(1,2)
        else: 
		    with open(filepath, 'wb') as f:
                    	f.write(form['file'].value)
			f.close()
		    	self.return_POST(1,0)

    def search_file(self,form,upload_path):
        filename = form['file'].filename
        filepath = os.path.join(upload_path, filename)
        compressionfile_path=upload_path+'/compress/compressionfile.list' 
	if os.path.exists(filepath):
		    self.return_POST(1,2)
	## FOR SEARCH COMPRESSED FILES
	elif os.path.exists(compressionfile_path) and filename in open(compressionfile_path).read():
		    self.return_POST(1,2)
	else:
		    self.return_POST(1,3)

    def delete_file(self,form,upload_path):
        filename = form['file'].filename
        filepath = os.path.join(upload_path, filename)
        compressionfile_path = upload_path+'/compress/compressionfile.list'
	if os.path.exists(filepath):
		    os.remove(filepath)
		    self.return_POST(1,4)
	## FOR IF FILE IS  COMPRESSED
	elif os.path.exists(compressionfile_path) and filename in open(compressionfile_path).read():
			## INIT SEARCHED = 0 AS NOT FOUND
		    searched = 0	
		    for line in reversed(open(compressionfile_path).readlines()):
    			if searched == 0 and filename in line:
				searched = 1
				continue
			if searched == 1 and line.startswith("compression-"):
			## TAR ZXVF COMPRESSION FILE AND REMOVE THE FILE AND TAR ZCVF AGAIN
				os.chdir(upload_path+'/compress/')			
				tar = tarfile.open(line[:-1])
				names = tar.getnames()
				tar.extractall()
				os.remove(filename)
				tar.close()
				tar = tarfile.open(line[:-1],"w:gz")
				for name in names:
					if name != filename:
						tar.add(name)
				tar.close()		
				for name in names:
					if name != filename:
						os.remove(name)		
				##REMOVE THE RECORD IN COMPRESSFILELIST
		    		f = open(compressionfile_path,"r")
		    		lines = f.readlines()
				f.close()
				##EMPTY THE FILE
				open(compressionfile_path,'w').close()
				f = open(compressionfile_path,"w")
                    		for l in lines:
                        		if not l[:-1].endswith(filename):
        					f.write(l)
				f.close()
				break
		    self.return_POST(1,4)
	else:
		    self.return_POST(1,3)


def run_server(HandlerClass = SimpleHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    run_server()
