from pymongo import MongoClient
client = MongoClient('localhost' , 27017)
db = client.userDetails

def checkUser(username , password):
	if db.table.find({"username" : username , "password" : password}).limit(1).count() > 0:
		return True
	else:
		return False


def addUser(username , password):
	if db.table.find({"username" : username}).limit(1).count() > 0:
		return False					## user already has an account
	else:
		row = {
		"username" : username ,
		"password" : password ,
		"filenames" : [] ,
		"files" : [] ,
		"links" : []
		}
		db.table.insert(row)
		return True


def addFile(username , filename , filecontent):
	if db.table.find({"username" : username , "filenames" : filename}).limit(1).count() > 0:
		return False     				## given file already exists
	else:
		db.table.update({ "username" : username } , {"$push" : { "filenames" : filename}})
		db.table.update({ "username" : username } , {"$push" : { "files" : {"filename" : filename , "filecontent" : filecontent }}})
		return True


def updateFile(username , filename , filecontent):
	if db.table.find({"username" : username , "filenames" : filename}).limit(1).count() == 0:
		return False 					## given file doesn't exists , can't be modified
	else:
		db.table.update({"username" : username , "files.filename" : filename} , { "$set" : {"files.$.filecontent" : filecontent}})
		return True


def getFileNames(username):
	if db.table.find({"username" : username}).limit(1).count() == 0:
		return False					## given username doesn't exists
	else:
		cursor = db.table.find({"username" : username}).limit(1)
		for item in cursor:
			#print item['filenames']
			return item['filenames']


def getFiles(username):
 	if db.table.find({"username" : username}).limit(1).count() == 0:
		return False					## given username doesn't exists
	else:
		cursor = db.table.find({"username" : username}).limit(1)
		for item in cursor:
			#print item["files"]
			return item["files"]


def getLinks(username):
	if db.table.find({"username" : username}).limit(1).count() == 0:
		return False					## given username doesn't exists
	else:
		cursor = db.table.find({"username" : username}).limit(1)
		for item in cursor:
			#print item["links"]
			return item["links"]


def addLink(username , linkbody):
	if db.table.find({"username" : username}).limit(1).count() == 0:
		return False					## given username doesn't exists
	else:
		db.table.update({"username" : username} , {"$push" : {"links" : linkbody}})
		return True

def escapeString(y):
	return y.replace('.' , '\\')

def descapeString(y):
	return y.replace('\\' , '.')