from flask import Flask , render_template , url_for , request , jsonify , session , redirect
import json , requests , hashlib
from databaseTransactions import *
from functools import wraps

app = Flask(__name__ , template_folder='templates')
app.secret_key = 'vabs22'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') != True:
            return redirect(url_for('loginpage'))
        return f(*args, **kwargs)
    return decorated_function


def user_not_logged_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') == True:
            return redirect(url_for('desktoppage'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def hello_world():
    return 'Welcome to cloudPc'

"""
@login_required
@app.route('/home')
def homepage():
	return render_template('home.html' , signupurl=url_for('signuppage') , loginurl = url_for('loginpage'))
"""


@app.route('/login')
@user_not_logged_required
def loginpage():
	return render_template('login.html' , SignupUrl=url_for('signuppage') , HomeUrl = url_for('desktoppage') , LoginUrl = url_for('loginuser'))



@app.route('/signup')
@user_not_logged_required
def signuppage():
	return render_template('signup.html' , LoginUrl = url_for('loginpage') , SignupUrl = url_for('signupuser'))


@app.route('/logout' , methods=['GET' , 'POST'])
@login_required
def logoutuser():
	session.clear()
	return redirect(url_for('loginpage'))



@app.route('/desktop')
@login_required
def desktoppage():
	return render_template('desktop.html' , compiler_url = url_for('compilerpage') , editor_url = url_for('editorpage') , player_url = url_for('mediaplayerpage'))



@app.route('/texteditor')
@login_required
def editorpage():
	return render_template('texteditor.html')



@app.route('/mediaplayer')
@login_required
def mediaplayerpage():
	return render_template('mediaplayer.html' , initUrl = url_for('get_mediaplayerpage_data') , linkUrl = url_for('linkdata') , playlistUrl = url_for('playlistdata'))



@app.route('/compiler')
@login_required
def compilerpage():
	return render_template('compiler.html' , compilingEndpoint = url_for('runcode'))


@app.route('/hackerrank' , methods=['GET', 'POST'])
@login_required
def runcode():
	data = json.loads(request.data)
	RUN_URL = 'http://api.hackerrank.com/checker/submission.json'
	key = 'hackerrank|304622-252|45b2fe94cc7186ee94f8f3e44620046cbcce9662'
	data = {
	    'api_key': key,
	    'source':  data['source'] , 
	    'lang': data['lang'],
	    'testcases': data['testcases'],
	    'format': 'json',
	}
	print str(data['testcases'])

	response = requests.post(RUN_URL, data=data)
	print str(response.text)
	return response.text


@app.route('/api/loginquery' , methods=['POST'])
@user_not_logged_required
def loginuser():
	data = json.loads(request.data)
	if request.method == 'POST':
		username = data['username']
		password = data['password']
	else:
		response = {'status' : 'error' , 'message' : 'Service Not supported'}
		return jsonify(response)

	response = {'status' : 'success' }
	result = verifyUser(username , password)
	uid = result["uid"]
	name = result["name"]
	if uid is not None and name is not None:
		response['result'] = 'true'
		session['logged_in'] = True
		session['uid'] = uid
		session['name'] = name
	else:
		response['status'] = "error"
		response['message'] = 'invalid Username or Password'
	return jsonify(response)



@app.route('/api/signupquery' , methods=['POST'])
@user_not_logged_required
def signupuser():
	data = json.loads(request.data)
	if request.method == 'POST':
		username = data['username']
		password = data['password']
		name = data['name']
	else:
		response = {'status' : 'error' , 'message' : 'Service Not supported'}
		return jsonify(response)
	
	uid = addUser(username , password , name)
	if uid is not None:
		response = {"status" : "success"}
	else:
		response = {"status" : "error" , "message" : "username already exists , please choose another username"}
	return jsonify(response)


"""

@app.route('/api/user/<operation>' , methods=['GET', 'POST'])
def userdata(operation):
	if request.method == 'GET':

	elif request.method == 'POST':

	else:
		response = {'status' : 'error' , 'message' : 'Service Not supported'}
		return str(response)

"""



@app.route('/api/file' , methods=['POST'])
@login_required
def filedata():
	data = json.loads(request.data)
	uid =  session['uid']
	operation = data["operation"]
	response = {}

	if operation == 'add':
		name = data['name']
		content = data['content']
		mode = data['mode']
		parent = data['parent']

		result = addFile(uid , name , content , parent , mode)
		if result:
			response = {"status" : "success"}
		else:
			response = {"status" : "error" , "message" : "A file with same name already exists"}

	elif operation == 'update':
		name = data['name']
		content = data['content']
		mode = data['mode']
		fid = data['fid']

		result = updateFile(fid , uid , name , content , mode)
		response = {"status" : "success"}

	elif operation == 'get':
		fid = data['fid']
		response = getFile(fid , uid)

	elif operation == 'del':
		response = {'status' : 'error' , 'message' : 'Service Not supported'}
	else:
		response = {'status' : 'error' , 'message' : 'Service Not supported'}

	return jsonify(response)


@app.route('/api/link' , methods=['POST'])
@login_required
def linkdata():
	data = json.loads(request.data)
	uid =  session['uid']
	operation = data["operation"]
	response = {}

	if operation == 'add':
		link = data["link"]
		name = data["name"]
		pid = int(data["playlist"])
		#print uid , name , link
		lid = addLink(uid , name , link)
		if lid is not None:
			result = addToPlaylist(uid , pid , lid)
			if result:
				response = {"status" : "success"}
			else:
				response = {"status" : "error" , "message" : "given link already exists in the playlist"}
		else:
			response = {"status" : "error" , "message" : "A file with same name already exists"}

	elif operation == 'get':
		lid = data['lid']
		response =  getLink(lid , uid)

	elif operation == 'update':
		lid = data['lid']
		link = data['link']
		name = data['name']

		result = updateLink(lid , uid , name , link)
		response = {"status" : "success"}

	elif operation == 'del':
		response = {'status' : 'error' , 'message' : 'Service Not supported'}
	else:
		response = {'status' : 'error' , 'message' : 'Service Not supported'}

	return jsonify(response)



@app.route('/api/playlist' , methods=['POST'])
@login_required
def playlistdata():
	data = json.loads(request.data)
	uid =  session['uid']
	operation = data["operation"]
	response = {}

	if operation == 'add':
		linklist = data['links']
		name = data['name']
		result = addPlaylist(uid , name , linklist)

		if result:
			response = {"status" : "success"}
		else:
			response = {"status" : "error" , "message" : "A file with same name already exists"}

	elif operation == 'get':
		pid = data['pid']
		response = getPlaylist(pid , uid)

	elif operation == 'update':
		response = {'status' : 'error' , 'message' : 'Service Not supported'}

	elif operation == 'del':
		response = {'status' : 'error' , 'message' : 'Service Not supported'}
	else:
		response = {'status' : 'error' , 'message' : 'Service Not supported'}

	return jsonify(response)



@app.route('/api/directory' , methods=['POST'])
@login_required
def directorydata():
	data = json.loads(request.data)
	uid =  session['uid']
	operation = data["operation"]
	response = {}

	if operation == 'add':
		name = data['name']
		parent = data['parent']
		fileList = []
		directoryList = []
		result = addDirectory(uid , name , fileList , directoryList , parent)

		if result:
			response = {"status" : "success"}
		else:
			response = {"status" : "error" , "message" : "A directory with same name already exists"}

	elif operation == 'get':
		did = data['did']
		response = getDirectory(did , uid)

	elif operation == 'del':
		response = {'status' : 'error' , 'message' : 'Service Not supported'}
	else:
		response = {'status' : 'error' , 'message' : 'Service Not supported'}

	return jsonify(response)

	

@app.route('/api/mediaplayer' , methods=['POST'])
@login_required
def get_mediaplayerpage_data():
	uid =  session['uid']
	response = {}

	links = getUserLinks(uid)
	linkdict = {}
	for link in links:
		linkdict[link] = getLink(link , uid)

	response["links"] = linkdict

	playlists = getUserPlaylists(uid)
	playlistdict = {}
	for playlist in playlists:
		playlistdict[playlist] = getPlaylist(playlist , uid)

	response["playlists"] = playlistdict

	return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8001 ,debug=True)