import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, flash
from supabase.client import Client, ClientOptions

from helpers import select_sorter

app = Flask(__name__)

# Useful for debugging
# app.config['SESSION_REFRESH_EACH_REQUEST'] = False

load_dotenv()

app.secret_key = os.environ.get("FLASK_APP_SECRET", "")
url = os.environ.get("SUPABASE_URL", "")
key = os.environ.get("SUPABASE_KEY", "")

supabase = Client(
    url,
    key,
    options=ClientOptions(
        flow_type="pkce"
    )
)


@app.route("/favicon.ico")
def favicon():
    return redirect("/static/favicon.ico")


@app.route('/')
def landing():
    is_auth = supabase.auth.get_user()

    info = {
        "title": "You are not logged in",
        "data": []
    }
    if is_auth is not None:
        data = supabase.table("starred").select("corpID, link:voting(graphLink), votes:voting(votes)").eq("user",
                                                                                                          is_auth.user
                                                                                                          .id).execute()
        print(data.data)
        if len(data.data) > 0:
            info["title"] = "Starred Corps"
            info["data"] = data.data
            return render_template("landingStarred.html", data=info)
        else:
            info["title"] = "No starred corps"

    return render_template('landing.html', data=info)


@app.route("/GetEmail", methods=["GET"])
def getEmail():
    try:
        data = supabase.auth.get_user()
        return jsonify(data.user.email)
    except AttributeError:
        return jsonify(None)


@app.route('/signin')
def signin():
    data = supabase.auth.get_user()
    if data is not None:
        return redirect('/')
    return render_template('signin.html')


@app.route('/signout')
def sign_out():
    supabase.auth.sign_out()
    return redirect('/')


@app.route('/change')
def changeLog():
    return render_template("changeBlogs.html")


@app.route('/chart')
def charts():
    is_auth = supabase.auth.get_user()
    if is_auth is None:
        return redirect('/signin')

    data = supabase.table("voting").select("*").eq("graphExists", True).execute()
    try:
        data = select_sorter(data.data)
    except IndexError:
        data = None
        flash("Something went wrong try again later")
    return render_template("charts.html", data=data)


@app.route("/vote")
def vote():
    is_auth = supabase.auth.get_user()
    if is_auth is None:
        return redirect('/signin')

    res = supabase.table("voting").select("*").eq("graphExists", False).execute()
    data = select_sorter(res.data)

    return render_template("vote.html", data=data)


@app.route("/handle_auth", methods=["POST"])
def handle_auth():
    email = request.form.get("user")
    password = request.form.get("pass")
    kind = request.form.get("type")

    if kind == "in":
        try:
            data = supabase.auth.sign_in_with_password({"email": email, "password": password})
            print(data)
            # return "JUDGEMENT"
            return redirect('/')
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
    d = supabase.table("voting").update({"votes": res.data[0]["votes"] + 1}).eq("Corporation Ticker value",
                                                                                ticker).execute()
    print(d)

    flash(f"Vote has been casted for {ticker}")
    return redirect('/vote')


@app.route("/handleStar", methods=["POST"])
def handleStar():
    is_auth = supabase.auth.get_user()
    if is_auth is None:
        return redirect('/signin')

    user_id = is_auth.user.id
    ticker = request.form.get("ticker")

    res = supabase.table("starred").select("*").eq("user", user_id).eq("corpID", ticker).execute()
    if len(res.data) > 0:
        flash("You have already starred this candidate")
        return redirect('/chart')

    res = (supabase.table("starred").insert({"user": user_id, "corpID": ticker}).execute())
    flash(f"{ticker} has been starred")
    return redirect('/chart')


if __name__ == '__main__':
    app.run(debug=True)
