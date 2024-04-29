# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Perform registration logic here
    # For simplicity, let's just print the registration data
    print(f"Received registration request - Username: {username}, Email: {email}, Password: {password}")

    return 'Registration successful!'

if __name__ == '__main__':
    app.run(debug=True)
