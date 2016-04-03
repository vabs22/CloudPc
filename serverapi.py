from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/loginquery')
def loginuser():


@app.route('/signupquery')
def signupuser():



@app.route('/logout')
def logoutuser():



@app.route('/desktopdata/<operation>')
def desktopdata():


@app.route('/file/<operation>')
def filedata():



@app.route('/link/<operation>')
def linkdata():


@app.route('/compilenrun')
def runcode():



if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8003 ,debug=True)