
import requests
from flask import Flask,render_template,url_for  # render_template is used to render the html file
#uel_for is used to get(hit) the url of the html file
import re

from flask import request as req  #requests and request both are different

#encapulating the code in a function 
app = Flask(__name__)
@app.route('/',methods=["GET","POST"]) #indentaion is important , this is the route of the main home page
def Index():
    return render_template("index.html") #rendering the html file , result will get displayed on html page

@app.route("/Summarize", methods = ["GET","POST"]) #this is the route of the summarization page
def Summarize():
    #if req.method=="POST":

        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer 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"}  #API used here is huggingface

        data = req.form["data"] #data is the name of the textarea in the html file

        #minL = 50
        #maxL = 100
        maxL = int(req.form["maxL"]) #maxL is the name of the input field in the html file
        minL = maxL//4
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        
        output = query(
            {
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
            }
        )[0] #accessing the first value of the output list
        result = output["summary_text"]

        counter = 0
        #counter = (len(re.findall(r'\w+', result)))
        counter = len(result.split())
        # for line in result:
        #     counter += line.count()
        #print(output) Here we have to send the output to the html file => Jinga2 can be used
        return render_template("index.html", result=result,counter=counter)

    #else:
        #return render_template("index.html")
    
    


if __name__ == "__main__":
    app.run(debug=True) #debug=True is used to run the code again and again without restarting the server
    # app.debug = True and app.run()
