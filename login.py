#building web applications in Python
from flask import Flask, request, render_template,redirect

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        id = request.form['username']
        name = request.form['password']
        # Perform registration logic here (e.g., storing username and password in a database)
        isExist = False
        f = open("D:\\Network\\NW_project2\\information", "a")
        with open("D:\\Network\\NW_project2\\information", "r") as file:
                for line in file:
                    if line.strip() == id:
                         isExist = True
        if not isExist:
            f.write(f"{id}\n")
            f.write(f"{name}\n")
            f.close()
        else:
             render_template("ID is exists")
             open("D:\\Network\\NW_project2\\hi.html", "r").read(1024)
        # Return a response to indicate successful registration
        return redirect(f'localhost:1001')
    #f'Registration successful! {username} '

    # Render the registration form template for GET requests
    return redirect(f'localhost:1001')

if __name__ == '__main__':
    app.run(debug=True)
