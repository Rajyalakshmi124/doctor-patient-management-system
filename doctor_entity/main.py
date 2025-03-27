from flask import Flask 
app = Flask(__name__) 
  
# Pass the required route to the decorator. 
@app.route("/") 
def hello(): 
    return "Hello, Welcome to Elixr"
  
if __name__ == "__main__": 
    app.run(debug=True)
