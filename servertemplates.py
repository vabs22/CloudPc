from flask import Flask , render_template , url_for
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


@app.route('/texteditor')
def editorpage():
	return render_template('texteditor.html')


@app.route('/mediaplayer')
def mediaplayerpage():
	return render_template('mediaplayer.html')


@app.route('/compiler')
def compilerpage():
	list_language = ['c++' , 'c' , 'python' , 'java']
	return render_template('compiler.html' , languages=list_language)


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8001 ,debug=True)