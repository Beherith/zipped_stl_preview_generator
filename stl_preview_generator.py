#100 lines or BUST by 2:00pm
import json
import pyunpack
import os
import shutil
import zipfile
import argparse

debug = False
dbfile = 'stl_preview_database.json'
dbfilebad = 'stl_preview_database_bad.json'
ztypes = ['.7z','.zip','.rar']
thumbdir = 'stl_previews'
tmpdir = 'tmp'

files_processed = [] #only process full zips
try:
	files_processed = json.loads(open(dbfile).read())
except:
	print ("Failed to open json database:", dbfile)

if not os.path.exists(thumbdir):
	os.mkdir(thumbdir)
if not os.path.exists(tmpdir):
	os.mkdir(tmpdir)

def ex(cmd):
	print (cmd)
	if not debug:
		return os.system(cmd)
	else:
		return 0

def isarchive(filename):
	for ztype in ztypes:
		if filename.lower().endswith(ztype):
			return True
	return False

def generate_preview(stlfilepath,previewfilename):
	#defaults: https://github.com/unlimitedbacon/stl-thumb/blob/master/src/config.rs
	#ambient: [0.0, 0.0, 0.4],
	#diffuse: [0.0, 0.5, 1.0],
	#specular: [1.0, 1.0, 1.0],
	OK = True
	stlthumb = 'stlthumb.png'
	previewpath = '%s%s%s.png'%(thumbdir,os.path.sep,previewfilename)
	if not os.path.exists(previewpath):
		print ("rendering",previewfilename)
		if ex('stl-thumb.exe "%s" "%s" -s 4096 -m 202020 908070 888888'%(stlfilepath,stlthumb)) ==0:
			if ex('convert.exe -quality 100 -resize 1024x1024 %s "%s%s%s.png"'%(stlthumb,thumbdir,os.path.sep,previewfilename)) ==0:
				print ('Success')
			else:
				OK = False
		else:
			OK = False
	else:
		print ("Already done:",previewpath)
	#stl-thumb.exe "Fighter - Threaded.stl" stlthumb.png -s 4096 -m 0x020204 0x908070 0xffffff
	if os.path.exists(stlthumb):
		ex('del %s'%(stlthumb))
	return OK,previewpath
def savedb(donefiles,dbfilename):
	try:
		s = json.dumps(donefiles)
	except:
		return
	f = open(dbfilename,'w')
	f.write(json.dumps(donefiles,indent=2))
	f.close()

def striptmp(instr):
	if instr.startswith(tmpdir):
		return instr.partition(os.path.sep)[2]
	else:
		return instr

def process_archive(archivepath, archivename, rootarchive = ''):
	OK = False
	print ("Processing", archivepath,archivename)
	try:
		pyunpack.Archive(os.path.join(archivepath,archivename)).extractall(os.path.join(tmpdir,archivename),auto_create_dir = True)
		process_folder(os.path.join(tmpdir,archivename),rootarchive = rootarchive+archivename+' [Z] ')
		OK = True
	except pyunpack.PatoolError:
		print ("ERROR: PATOOL ERROR, UNABLE TO UNZIP", rootarchive, archivepath, archivename)
		OK = False
	except IOError:
		print ("ERROR: IOERROR, UNABLE TO UNZIP",rootarchive, archivepath, archivename)
		OK = False
	except zipfile.BadZipfile:
		OK = False
		print ("ERROR: zipfile.BadZipfile",rootarchive, archivepath, archivename)
	except ValueError:
		OK = False
		print ("ERROR: ValueError, archive does not exist!",rootarchive, archivepath, archivename)
 	try:
		shutil.rmtree('%s'%(os.path.join(tmpdir,archivename)))
	except WindowsError:
		print ("WARNING: Unable to delete folder", os.path.join(tmpdir,archivename))
	return OK

def process_folder(rootpath,rootarchive = ''):
	print ("Processing: ",rootarchive,rootpath)
	goodfiles = 0
	badfiles = 0
	for root,dirs,files in os.walk(rootpath):
		for name in files:
			if isarchive(name):
				if name not in files_processed:
					process_archive(root,name,rootarchive = rootarchive)
					try:
						json.dumps([name])
						files_processed.append(name)
					except:
						print ("ERROR: Unable to decode file name:",name)
					savedb(files_processed,dbfile)
				else:
					print ("Skipping file already in database:",root,name)
			if name.lower().endswith('.stl') and rootarchive != '': #dont process naked stls?
				name = os.path.join(root,name)
				fullpath = rootarchive + striptmp(name.replace(rootpath+os.path.sep,''))
				previewfilename = fullpath.replace(os.path.sep, ' [D] ')
				generate_preview(name,previewfilename)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--folder", required = True, help="The path to the folder to be processed")
	args = parser.parse_args()
	process_folder(args.folder)
