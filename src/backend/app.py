import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, flash

from supabase_client import supabase

app = Flask(__name__)

load_dotenv()

app.secret_key = os.environ.get("FLASK_APP_SECRET", "")


@app.route('/')
def landing():
    return render_template('root.html')


@app.route("/GetEmail", methods=["GET"])
def getEmail():
    try:
        data = supabase.auth.get_user()
        return jsonify(data.user.email)
    except Exception as e:
        return jsonify(None)


@app.route('/voting')
def voting():
    return ""


@app.route('/signin')
def signin():
    data = supabase.auth.get_user()
    if data is not None:
        return redirect('/')
    return render_template('signin.html')


@app.route('/signout')
def signout():
    res = supabase.auth.sign_out()
    return redirect('/')


@app.route('/change')
def changeLog():
    return render_template("changeBlogs.html")


@app.route("/vote")
def vote():
    is_auth = supabase.auth.get_user()
    if is_auth is None:
        return redirect('/signin')

    res = supabase.table("voting").select("*").execute()
    data = []

    for i in res.data:
        # print(i)
        data.append([i["Corporation Name"], i["Corporation Ticker value"], i["votes"]])

    return render_template("vote.html", data=data)


@app.route("/handle_auth", methods=["POST"])
def handle_auth():
    email = request.form.get("user")
    password = request.form.get("pass")
    kind = request.form.get("type")

    if kind == "in":
        try:
            data = supabase.auth.sign_in_with_password({"email": email, "password": password})

            # return str(data)
        except Exception as e:
            flash(str(e))
            return redirect('/signin')
    else:
        try:
            data = supabase.auth.sign_up(credentials={"email": email, "password": password})
            print(data)
            flash("User has been created.... please sign in")
            return redirect('/signin')
            # return "User has been created.... Go back and sign in"

        except Exception as e:
            flash(str(e))
            return redirect('/signin')

    return redirect('/')


@app.route("/handleVote", methods=["POST"])
def handleVote():
    is_auth = supabase.auth.get_user()
    if is_auth is None:
        return redirect('/signin')

    ticker = request.form.get("candidate")

    res = supabase.table("userVoterRelation").select("*").eq("user", is_auth.user.id).eq("corpID", ticker).execute()
    if len(res.data) > 0:
        flash("You have already voted for this candidate")
        return redirect('/vote')
        # return "You have already voted for this candidate"

    res = supabase.table("voting").select("*").eq("Corporation Ticker value", ticker).execute()
    supabase.table("userVoterRelation").insert({"user": is_auth.user.id, "corpID": ticker}).execute()
    supabase.table("voting").update({"votes": res.data[0]["votes"] + 1}).eq("Corporation Ticker value",
                                                                            ticker).execute()

    flash(f"Vote has been casted for {ticker}")
    return redirect('/vote')


if __name__ == '__main__':
    app.run(debug=True)
