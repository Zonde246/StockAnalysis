from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect

from supabase_client import supabase

app = Flask(__name__)

app.secret_key = ("console prenatal carefully thousand hydroxide nursery antarctic cataract idiocy partly graveyard "
                  "mortify curtly decency swagger")

load_dotenv()


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
    return render_template('signin.html')


@app.route('/signout')
def signout():
    res = supabase.auth.sign_out()
    return redirect('/')


@app.route('/change')
def changeLog():
    return render_template("changeBlogs.html")


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
            return str(e)
    else:
        try:
            data = supabase.auth.sign_up(credentials={"email": email, "password": password})
            print(data)
            return "User has been created.... Go back and sign in"
        except Exception as e:
            return str(e)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
