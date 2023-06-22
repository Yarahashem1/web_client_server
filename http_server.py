import socket
import threading
from http_request import Httpp

# Define constants for the server
HOST = 'localhost'
PORT = 1001
MAX_CLIENTS = 5


# Create a dictionary to hold all connected clients and their usernames
connected_clients = {}

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # IPv4 addresses. & TCP connectiomn

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(MAX_CLIENTS)



# HTML for the login page
login_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Registration Page</title>
  <style>
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f2f2f2;
      font-family: Arial, sans-serif;
    }
    .container {
      width: 400px;
      background-color: #fff;
      border-radius: 5px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      padding: 40px;
    }
    .container h1 {
      margin-top: 0;
      text-align: center;
      color: #333;
    }
    .form-group {
      margin-bottom: 20px;
    }
    .form-group label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
      color: #555;
    }
    .form-group input {
      width: 100%;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 3px;
      font-size: 16px;
    }
    .form-group input[type="submit"] {
      background-color: #4caf50;
      color: #fff;
      cursor: pointer;
    }
    .form-group input[type="submit"]:hover {
      background-color: #45a049;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Registration Page</h1>
    <form method="post" action="http://localhost:5000/register">
      <div class="form-group">
        <label for="username">ID:</label>
        <input type="text" id="username" name="username">
      </div>
      <div class="form-group">
        <label for="password">Name:</label>
        <input type="text" id="password" name="password">
      </div>
      <div class="form-group">
        <input type="submit" value="Register">
      </div>
    </form>
  </div>
</body>
</html>
"""
# Function to handle incoming client connections
def handle_client_send(client_socket, client_address):
    req = client_socket.recv(1024).decode()        # 1024 specifies the maximum number of bytes to be received at once.from byte to String
    http_anatomical = Httpp(req)
    req = http_anatomical.get_query_param()
    if not req:
        # Send the login page HTML
        body = login_page
        body_length = len(body)
        #http response header
        headers = f"""HTTP/1.1 200 OK    
Content-Type: text/html charset=UTF-8
content-length: {body_length}

"""           #the request was successful   #the length of the response 
        response = headers + body
        client_socket.send(response.encode())  
        client_socket.close()
    else:
        try:
            id = ""
            count = 0
            name = ""
            with open("D:\\Network\\NW_project2\\information", "r") as file:
                for line in file:
                    
                    if line.strip() == req:  #removing leading and trailing whitespaces 
                        id = line
                        count = 1
                        continue
                    if count == 1:
                        name = line
                        break
            year = id[1:5]
            level = 2023 - int(year)
            if level > 5:
                level = "graduated!"
            university_results = f"""
    <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; color: #333333; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px; border-radius: 5px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
          <h1 style="font-size: 32px; margin-bottom: 30px; color: #333333;">Results</h1>
          
          <div style="text-align: left;">
            <p style="font-size: 18px; margin-bottom: 10px;"><strong>ID:</strong> {id}</p>
            <p style="font-size: 18px; margin-bottom: 10px;"><strong>Name:</strong> {name}</p>
            <p style="font-size: 18px; margin-bottom: 10px;"><strong>Level:</strong> {level}</p>
          </div>
          <div style="margin-top: 40px;">
            <a href="http://example.com" style="background-color: #4caf50; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-size: 18px;">Continue</a>
          </div>
        </div>
      </body>
    """
        except ValueError:
            university_results = f"""

                              <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; color: #333333; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px; border-radius: 5px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
          <h1 style="font-size: 32px; margin-bottom: 30px; color: #333333;">Invalid ID!. Please try again with correct ID.</h1>
          
         
          <div style="margin-top: 40px;">
            <a href="http://example.com" style="background-color: #4caf50; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-size: 18px;">Continue</a>
          </div>
        </div>
      </body>"""
    # client_socket.close()
    body  = f"""<html><body>{university_results}</body></html>"""
    body_length = len(body)
    headers = f"""HTTP/1.1 200 OK
Content-Type: text/html charset=UTF-8
content-length: {body_length}

"""
    response = headers + body
    client_socket.send(response.encode())    #string to byte
    client_socket.close()

# Main loop to handle incoming connections
while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()
    
    # Create a new thread to handle the client connection
    client_thread_send = threading.Thread(
        target=handle_client_send, args=(client_socket, client_address))
    client_thread_send.start()
    



    