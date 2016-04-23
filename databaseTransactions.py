from pymongo import MongoClient
client = MongoClient('localhost' , 27017)
db = client.cloudPc

"""

Schema :

S.No      Collections      Document attributes   
1. 			Users 			uid , username , password , name  ### empty at the moment, files([fid]) , links([lid]) , playlists([pid]) , directory([fid] , [did])
2. 			Files			fid , uid , parent , name , content
3. 			Links			lid , uid , link , name
4. 			Playlists		pid , uid , name , links([lid])
5. 			Directories		did , uid , parent , name , files([fid]) , directories([did])

#cursor = db.Users.find().sort({uid:-1}).limit(1)
"""

def getUidCounter():
	cursor = db.Users.find().sort([(u'uid' , -1)]).limit(1)
	uid = 0
	for document in cursor:
		uid = document["uid"]
	return uid + 1

def getFidCounter():
	cursor = db.Files.find().sort([(u'fid' , -1)]).limit(1)
	fid = 0
	for document in cursor:
		fid = document["fid"] 
	return fid + 1

def getLidCounter():
	cursor = db.Links.find().sort([(u'lid' , -1)]).limit(1)
	lid = 0
	for document in cursor:
		lid = document["lid"] 
	return lid + 1

def getPidCounter():
	cursor = db.Playlists.find().sort([(u'pid' , -1)]).limit(1)
	pid = 0
	for document in cursor:
		pid = document["pid"] 
	return pid + 1

def getDidCounter():
	cursor = db.Directories.find().sort([(u'did' , -1)]).limit(1)
	did = 0
	for document in cursor:
		did = document["did"] 
	return did + 1

def getFileName(fid , uid):					# returns filename
	fid = int(fid)
	uid = int(uid)
	cursor = db.Files.find({ "fid" : fid  , "uid" : uid})
	filename = None
	for document in cursor:
		filename = document["name"]
	return  filename

def getFile(fid , uid):						# returns file content
	fid = int(fid)
	uid = int(uid)
	cursor = db.Files.find({ "fid" : fid , "uid" : uid})
	filecontent = None
	for document in cursor:
		filecontent = document["content"]
	return  filecontent

def getLink(lid , uid):						# returns linkname , link pair
	lid = int(lid)
	uid = int(uid)
	cursor = db.Links.find({ "lid" : lid , "uid" : uid})
	linkname = None
	link = None
	for document in cursor:
		linkname = document["name"]
		link = document["link"]
	return  linkname,link

def getPlaylistName(pid , uid):				# returns playlist name
	pid = int(pid)
	uid = int(uid)
	cursor = db.Playlists.find({ "pid" : pid , "uid" : uid})
	name = None
	for document in cursor:
		name = document["name"]
	return  name

def getPlaylist(pid , uid):					# returns [lid] in playlist
	pid = int(pid)
	uid = int(uid)
	cursor = db.Playlists.find({ "pid" : pid , "uid" : uid})
	playlist = None
	for document in cursor:
		playlist = document["links"]
	return  playlist

def getDirectoryName(did , uid):				# returns directory name
	did = int(did)
	uid = int(uid)
	cursor = db.Directories.find({ "did" : did , "uid" : uid})
	name = None
	for document in cursor:
		name = document["name"]
	return  name

def getDirectory(did , uid):					# returns [fid] , [did] pair
	did = int(did)
	uid = int(uid)
	cursor = db.Directories.find({ "did" : did , "uid" : uid})
	files = None
	directories = None
	for document in cursor:
		files = document["files"]
		directories = document["directories"]
	return  files,directories

def getUserLinks(uid):					# returns [lid]
	uid = int(uid)
	cursor = db.Users.find({ "uid" : uid})
	links = None
	for document in cursor:
		links = document["links"]
	return links

def getUserPlaylists(uid):				# returns [pid]
	uid = int(uid)
	cursor = db.Users.find({ "uid" : uid})
	playlists = None
	for document in cursor:
		playlists = document["playlists"]
	return playlists

def getUserDirectory(uid):				# returns [did]
	uid = int(uid)
	cursor = db.Users.find({ "uid" : uid})
	directories = None
	files = None
	for document in cursor:
		directories = document["directory"]["directories"]
		files = document["directory"]["files"]
	return files,directories

def getUserFiles(uid):					# returns [fid]
	uid = int(uid)
	cursor = db.Users.find({ "uid" : uid})
	files = None
	for document in cursor:
		files = document["files"]
	return files

def verifyUser(username , password):	# returns uid or none
	cursor = db.Users.find({"username" : username , "password" : password}).limit(1)
	uid = None
	for document in cursor:
		uid = document["uid"]
	return uid

def addUser(username , password , name):		# returns True or false
	if db.Users.find({"username" : username}).limit(1).count() > 0:
		return None					## user already has an account
	else:
		uid = getUidCounter()
		row = {
		"uid" : uid , 
		"username" : username ,
		"password" : password ,
		"name" : name ,
		"files" : [] ,
		"links" : [] , 
		"playlists" : [] ,
		"directories" : []
		}
		db.Users.insert(row)

		didrow = {
		"did" : 0 ,
		"uid" : uid , 
		"name" : "root" , 
		"parent" : -1 ,
		"files" : [] ,
		"directories" : []
		}
		db.Directories.insert(didrow)
		return uid

def addFile(uid , name , content , parent):
	uid = int(uid)
	parent = int(parent)
	flag = True
	cur = db.Files.find({"uid" : uid , "name" : name , "parent" : parent})
	for row in cur:
		flag = False
	if flag:
		fid = getFidCounter()
		filedoc = {
		"fid" : fid , 
		"uid" : uid , 
		"parent" : parent ,
		"name" : name , 
		"content" : content 
		}

		db.Files.insert(filedoc)
		db.Directories.update({ "uid" : uid , "did" : parent } , {'$push' : { 'files' : fid}})
		db.Users.update({"uid" : uid} , {'$push' : {'files' : fid}})
		return True
	else:
		return False

def addDirectory(uid , name , fileList , directoryList , parent):
	uid = int(uid)
	parent = int(parent)
	flag = True
	cur = db.Directories.find({"uid" : uid , "name" : name , "parent" : parent})
	for row in cur:
		flag = False
	if flag:
		did = getDidCounter()
		directorydoc = {
		"did" : did , 
		"uid" : uid , 
		"parent" : parent ,
		"name" : name , 
		"files" : [] , 
		"directories" : []
		}

		db.Directories.insert(directorydoc)
		db.Directories.update({ "uid" : uid , "did" : parent } , {'$push' : { 'directories' : did}})
		db.Users.update({"uid" : uid} , {'$push' : {'directories' : did}})
		return True
	else:
		return False

def addLink(uid , name , link):
	uid = int(uid)
	flag = True
	cur = db.Links.find({"uid" : uid , "name" : name , "link" : link})
	for row in cur:
		flag = False
	if flag:
		lid = getLidCounter()
		linkdoc = {
		"lid" : lid , 
		"uid" : uid ,
		"name" : name , 
		"link" : link
		}
		db.Links.insert(linkdoc)
		db.Users.update({"uid" : uid} , {'$push' : {'links' : lid}})
		return True
	else:
		return False

def addPlaylist(uid , name , linklist):
	uid = int(uid)
	flag = True
	cur = db.Playlists.find({"uid" : uid , "name" : name })
	for row in cur:
		flag = False
	if flag:
		pid = getPidCounter()
		playlistDoc = {
		"pid" : pid , 
		"uid" : uid , 
		"name" : name ,
		"links" : linklist
		}
		db.Playlists.insert(playlistDoc)
		db.Users.update({"uid" : uid} , {'$push' : {'playlists' : pid}})
		return True
	else:
		return False


def addToPlaylist(uid , pid , lid):
	uid = int(uid)
	pid = int(pid)
	lid = int(lid)
	flag = True
	cur = db.Playlists.find({"uid" : uid , "pid" : pid , "links" : lid })
	for row in cur:
		flag = False
	if flag:
		db.Playlists.update({"uid" : uid , "pid" : pid} , {'$push' : {'links' : lid}})
		return True
	else:
		return False

"""

def updateFile(fid , uid , name , content):
	db.Files.update({"uid" : uid , "fid" : fid} , { "$set" : {"name" : name , "content" : content}})

def updateLink(lid , uid , name , link):
	db.Links.update({"uid" : uid , "lid" : lid} , { "$set" : {"name" : name , "link" : link}})

def updateDirectory(did , uid , name):
	db.Directories.update({"uid" : uid , "did" : did} , { "$set" : {"name" : name}})

def updatePlaylist(uid , pid , name):
	db.Playlists.update({"uid" : uid , "pid" : pid} , { "$set" : {"name" : name}})

def delFile(uid , fid , parent):
	db.Files.remove({"uid" : uid , "fid" : fid})
	db.Directories.update({"uid" : uid , "did" : parent} , {"$pull" : {"files" : fid}})

def delLink(uid , lid)

"""		
