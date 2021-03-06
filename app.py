from flask import Flask, render_template, request, redirect, session, url_for
import login_utils, tasks_utils
application = Flask(__name__)


@application.route("/", methods=['GET','POST'])
@application.route("/home", methods=['GET','POST'])
def home():
    if 'logged_in' not in session:
        session['logged_in'] = False
    if 'user' not in session:
        session['user'] = 'Guest'
#    return render_template('home.html')
    if request.method=="GET":
        return render_template('home.html')
    else:
        button = request.form['button']
        if button == "Create Account":
            user = request.form['new_username']
            password = request.form['new_password']
            confirm = request.form['new_confirm_password']
            #password match check
            if (password == confirm):
                #username and password lengths check
                if "@" not in user:
                    return render_template('home.html',errorC="Username must be a valid email")
                if len(password)<8:
                    return render_template('home.html',errorC="Password must be longer than 8 characters")
                #account created successfully
                if  login_utils.create_user(user,password):
                    return render_template('home.html',successC="Account successfully created! Login to access DailyDos.")
                #username taken error
                else:
                    return render_template('home.html',errorC="Username already in use. Please chose a different username")            
            else:
                return render_template('home.html',errorC="Passwords do not match")
        #Login
        #if credentials valid, log them in with session
        if button == "Login":
            user = request.form['login_username']
            password = request.form['login_password']
            if login_utils.authenticate(user,password):
                session['user'] = user
                session['logged_in'] = True
                return redirect(url_for('tasks'))
                #else renders login w/ error message
            else:
                return render_template("home.html",errorL="Invalid Username or Password")
                
@application.route("/tasks", methods=["GET","POST"])
def tasks():
    tasks_list = tasks_utils.get_tasks(session['user'])
    if session['logged_in'] == False:
        return redirect('/home')
    if request.method == "GET":
        return render_template("tasks.html", tasks = tasks_list)
    if request.method == "POST":
        button = request.form['button']
        if button == "Remove These":
            #page_ids = request.form.get("do_delete")
            checked = request.form.getlist("checks")
            #checked = []
            #for items in request.form.get("do_delete"):
            #    checked.append(items)
            #selected = bool(checked)
            #f = open('log_file', 'w')
            #for keys in selected:
            #    f.write(selected)
            #f.close()
            
            tasks_utils.remove_tasks(checked)
            tasks_list = tasks_utils.get_tasks(session['user'])
            return render_template("tasks.html", tasks = tasks_list)
        if button == "Clear All":
            tasks_utils.clear_tasks(session['user'])
            tasks_list = tasks_utils.get_tasks(session['user'])
            return render_template("tasks.html", tasks = tasks_list)
        else:
            return render_template("tasks.html", tasks = tasks_list)

@application.route("/logout")
def logout():
    session['user'] = "Guest"
    session['logged_in'] = False
    return redirect('/home')

application.secret_key = "pleasework"

if __name__=="__main__":

    application.run(host='0.0.0.0')
    """
    application.debug = True
    application.secret_key = "onetwothreefour"
    application.run(host='0.0.0.0', port = 5000)
    """
