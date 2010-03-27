# -*- coding: utf-8 -*-

import os
import string

def crawlDir(directory, list):
	"runs through a specified directory tree and adds folders which match the conditions to list"
		
	#get filelist
	fileList = [os.path.normcase(f)
			for f in os.listdir(directory) 
			if os.path.isfile(os.path.join(directory,f))]
		
	#get dirlist
	dirList = [os.path.normcase(f)
			for f in os.listdir(directory) 
			if os.path.isdir( os.path.join( directory,f ))]
	
	#apply filters
	containsMp3 = False
	containsSourceExt = False
	
	for f in fileList:
		if os.path.splitext(f)[1] in sourceExt and not containsSourceExt:
			containsSourceExt = True
			
	if containsSourceExt:
		list.append(directory)

    #apply recursively to all folders in tree
	for d in dirList:
		crawlDir(os.path.join(directory, d),list)

def processList(list):
	"runs through list, creates folder structure in destDir and converts .flac files to mp3"
	for d in list:
		newPath = d.replace(sourceDir,destDir)
		if not os.path.exists(newPath):
			os.makedirs(newPath)
			convertToMp3(d,newPath)

def convertToMp3(src,dst):
	"converts files contained in src to mp3 files in dst"
	fileList = [f
			    for f in os.listdir(src)
			    if os.path.isfile(os.path.join(src,f)) and os.path.splitext(f)[1] == ".flac"]
	for f in fileList:
		srcFile = os.path.join(src,f)
		tmpFile = os.path.join(dst,(os.path.splitext(f)[0] + ".wav"))
		dstFile = os.path.join(dst,(os.path.splitext(f)[0] + ".mp3"))
		
		os.spawnlp(os.P_WAIT, "flac", "flac", "-d",srcFile, "-o", tmpFile, )
		os.spawnlp(os.P_WAIT, "lame","lame","-h","-b",bitRate, tmpFile, dstFile)
		os.remove(tmpFile)

def verifySettings():
	print "============================="
	print "sourceDir: " + sourceDir
	print "destDir: " + destDir
	print "sourceExt: " + sourceExt.__str__()
	print "bitRate: " + bitRate
	print "============================="
	input = raw_input("are these settings correct? y/N ")
	
	return (input == "Y" or input == "y" )

#global vars

sourceDir="/home/jakob/mp3"
destDir="/home/jakob/mp3mirror"
sourceExt= [".flac"]
bitRate= "192"
dirList = []

#main

if __name__ == "__main__":
	
	if not verifySettings():
		exit
		
	crawlDir(sourceDir, dirList)
	
	processList(dirList)
