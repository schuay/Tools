# -*- coding: utf-8 -*-
import sys
import re
import os
import stat
import shutil

path_to_process = ""
op= "-l"

class fsObject:
  name = ""
  newName = ""
  isDir = False
  nr = 0
  
  def __init__(self,path,newPath):
	full_path = os.path.join(path_to_process, path)
	self.name = path
	self.newName = newPath
	self.isDir = os.path.isdir(full_path)
  def __str__(self):
	return self.name
  
def cleanName(originalName):
  fullName=os.path.join(path_to_process,fname)
  originalName=originalName.lower()

  isDir=os.path.isdir(fullName)

  #skip files smaller than 30 megs
  if not isDir and os.stat(fullName)[stat.ST_SIZE] < 1024*1000*30:
	return originalName

  #remove known bad portions of strings ([], (), dvdrip,xvid, etc)
  wrkStr=re.sub(r'\[.*?\]', '', originalName)
  wrkStr=re.sub(r'\(.*?\)', '', wrkStr)
  wrkStr=re.sub(r'dvdrip', '', wrkStr)
  wrkStr=re.sub(r'xvid', '', wrkStr)

  #convert all separators to _
  wrkStr=re.sub(r'[\._]', ' ', wrkStr) #convert all separators to space
  wrkStr=re.sub(r' +', '_', wrkStr.lstrip().rstrip()) 	#trim, then convert whitespace to _

  #restore dot before file extension
  if not isDir:
	wrkStr=re.sub(r'(.*)_(....?$)', r'\1/\1.\2', wrkStr) 

  return wrkStr
  
def displayResults(results):
  changed = 0
  unchanged = 0

  for k in results:
	if k.name != k.newName:
	  status = "[X]"
	  changed += 1
	else:
	  status = "[-]"
	  unchanged += 1

	print '{0:2d} - {1:4s}{2:30s} --> {3}'.format(k.nr, status, k.name, k.newName)

  print '\nchanged: {0} unchanged: {1}'.format(changed, unchanged)
  
def applyChanges(results):
  if op != "-c":
	return
	
  input = raw_input("apply changes? (N/y): ")
  if input in ("", "n", "N"):
	print "no changes applied"
	return
	
  changed = 0
	
  for k in results:
	if k.name != k.newName:
	  src=os.path.join(path_to_process,k.name)
	  dst=os.path.join(path_to_process,k.newName)
	  
	  if not os.path.exists(os.path.dirname( dst) ):
		os.mkdir(os.path.dirname(dst))

	  shutil.move(src, dst)
	  changed += 1
	  
	  print '{0:2d} - {1:30s} --> {2}'.format(k.nr, k.name, k.newName)

  print '\n{0} files/directories processed successfully'.format(changed)

def nameCompare(x, y):
  if x.name > y.name:
	  return 1
  elif x.name == y.name:
	  return 0
  else: 
	  return -1
	  
def sortResults(dirTargetListClass):
  dirTargetListClass.sort(nameCompare)
  
  i=0
  for c in dirTargetListClass:
	c.nr = i
	i+=1
	
def customizeResults(dirTargetListClass):
  input = raw_input("customize? (N/l/nr): ")
  
  if input in ("", "n", "N"):
	return True
	
  if input in ("l", "L"):
	displayResults(dirTargetListClass)
	return False
	
  try: 
	i=int(input)
  except ValueError:
	print "incorrect value entered"
	return False
	
  def f(x): return x.nr == i
  	
  entry = filter(f, dirTargetListClass)
  
  if len(entry) < 1:
	print "number not found"
	return False
  
  print "{0:30s} --> {1}".format(entry[0].name, entry[0].newName)
  entry[0].newName = raw_input("new file destination: ")
  print "{0:30s} --> {1}".format(entry[0].name, entry[0].newName)
  
  return False

if __name__ == "__main__":

  if len(sys.argv) != 3:
	print "usage: argv[1]={-l (list), -c (change), argv[2]=path"
	sys.exit(1)
	
  op = sys.argv[1]
  path_to_process = sys.argv[2]
	
  if not os.path.exists(path_to_process) or op not in ("-l", "-c"):
	print "path doesn't exist or wrong operation"
	sys.exit(1)

  dirList=os.listdir(path_to_process)
  dirTargetListClass=[]

  for fname in dirList:
	dirTargetListClass.append(fsObject(fname,cleanName(fname)))
	
  sortResults(dirTargetListClass)
  displayResults(dirTargetListClass)
  
  cont = False
  while not cont:
	cont = customizeResults(dirTargetListClass)
	
  applyChanges(dirTargetListClass)
