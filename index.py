from flask import Flask,render_template
import os,openai
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db=SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

def register()->object:
    with app.app_context:
        db.create_all()
        db.session.add(User(username="akshay"))
        db.session.commit()
        users=db.session.execute(db.select(User)).scalars()
        return users


openai.api_key = "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"


def connect_to_essay(topic)->str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Write a good essay on {topic} in minimum 2500 words",
        temperature=1.0,
        max_tokens=2800,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.5
        )
    
    return response


def connect_to_food(recipe)->str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Write a recipe based on these ingredients and instructions:\n\n{recipe}\nIngredients:\nInstructions:",
        temperature=1.0,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.3,
        presence_penalty=0.3
        )
    
    return response,connect_to_image(recipe)

def connect_to_image(recipe)->str:
    response = openai.Image.create(
        prompt=f"A perfect image related to this information whether a food or topic or emotion:\n\n{recipe}\nInstructions:",
        n=1,
        size="256x256"
        )
    return response["data"][0]["url"]

def connect_to_pov(recipe)->str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Can you reluctantly answer this question with sarcastic responses:\n\n{recipe}",
        temperature=1.0,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.3,
        presence_penalty=0.3
        )
    return response,connect_to_image(recipe)

def connect_to_study(recipe)->str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"What are 10 key points I should know when studying Ancient {recipe}?",
        temperature=1.0,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.3,
        presence_penalty=0.3
        )
    return response,connect_to_image(recipe)

@app.route("/essay/<topic>",methods=["GET"])
def write_essay(topic):
    return render_template("essay.html",instr=connect_to_essay(topic)["choices"][0]["text"])

@app.route("/index",methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/food/<recipe>",methods=["GET"])
def show_food(recipe):
    return render_template("food.html",instr=connect_to_food(recipe)[0]["choices"][0]["text"],furl=connect_to_food(recipe)[1])

@app.route("/notes/<topic>",methods=["GET"])
def show_notes(topic):
    return render_template("study.html",instr=connect_to_study(topic)[0]["choices"][0]["text"],furl=connect_to_study(topic)[1])


@app.route("/pov/<pov>",methods=["GET"])
def show_pov(pov):
    return render_template("pov.html",instr=connect_to_pov(pov)[0]["choices"][0]["text"],furl=connect_to_pov(pov)[1])



if __name__=="__main__":
    app.run("localhost",8081,debug=False)
