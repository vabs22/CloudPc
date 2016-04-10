from flask import Flask , render_template , url_for , request
import json , requests

app = Flask(__name__ , template_folder='templates')

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def homepage():
	return render_template('home.html' , signupurl=url_for('signuppage') , loginurl = url_for('loginpage'))


@app.route('/login')
def loginpage():
	return render_template('login.html' , signupurl=url_for('signuppage'))


@app.route('/signup')
def signuppage():
	return render_template('signup.html' , loginurl = url_for('loginpage'))


@app.route('/desktop')
def desktoppage():
	return render_template('desktop.html' , compiler_url = url_for('compilerpage') , editor_url = url_for('editorpage') , player_url = url_for('mediaplayerpage'))


@app.route('/hackerrank' , methods=['GET', 'POST'])
def runcode():
	#print str(request.data)
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
	#print str(data['testcases'])

	response = requests.post(RUN_URL, data=data)
	#print str(response.text)
	return response.text


@app.route('/texteditor')
def editorpage():
	return render_template('texteditor.html')


@app.route('/mediaplayer')
def mediaplayerpage():
	return render_template('mediaplayer.html')


@app.route('/compiler')
def compilerpage():
	return render_template('compiler.html' , compilingEndpoint = url_for('runcode'))


@app.route('/api/loginquery' , methods=['GET', 'POST'])
def loginuser():
	return ""

@app.route('/api/signupquery' , methods=['GET', 'POST'])
def signupuser():
	return ""


@app.route('/api/logout' , methods=['GET', 'POST'])
def logoutuser():
	return ""


@app.route('/api/desktopdata/<operation>' , methods=['GET', 'POST'])
def desktopdata():
	return ""

@app.route('/api/file/<operation>' , methods=['GET', 'POST'])
def filedata():
	return ""


@app.route('/api/link/<operation>' , methods=['GET', 'POST'])
def linkdata():
	return ""
	

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8001 ,debug=True)