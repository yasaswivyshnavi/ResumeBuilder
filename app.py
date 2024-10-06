from flask import *
import pymysql
import os
import uuid
app = Flask(__name__)
app.secret_key = "egeiuhfeufheiofeipruw123245"  #secret_key

def dbconn():
    try:
        conn = pymysql.connect(
            host = "localhost",
            user = "root",
            password="",
            db = "resume"
        )
        print("db is connected")
        cursor = conn.cursor()
        return cursor,conn
    except Exception as e:
        print(f"{e}")
        exit



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/templatesPage')
def templatesPage():
    if session.get('name') is  None:
        return redirect("/login")
    # elif session.get('uname') is None:
    #     return redirect("/form")
    
    return render_template('templatesPage.html')

#template pages
# template1
@app.route('/template1')
def template1():

    if session.get('name') is None:
        return redirect("/login")
    # elif session.get('uname') is  None:
    #     return redirect("/form")
    
    return render_template('template1.html')

# template1
@app.route('/template2')
def template2():

    if session.get('name') is None:
        return redirect("/login")
    # elif session.get('uname') is  None:
    #     return redirect("/form")
    
    return render_template('template2.html')

# template3
@app.route('/template3')
def template3():

    if session.get('name') is None:
        return redirect("/login")
    # elif session.get('uname') is  None:
    #     return redirect("/form")
    
    return render_template('template3.html')

@app.route('/signup',methods=["GET","POST"])
def signup():
    cursor,conn = dbconn()
    if request.method == "POST":
        username = request.form['uname'].strip()
        email = request.form['email'].strip()
        mobile = request.form['mobile'].strip()
        pwd = request.form['pwd'].strip()
        cpwd = request.form['cpwd'].strip()
        if (username=="") or (email=="") or (mobile=="") or (pwd=="") or (cpwd==""):
            print("give all details")
            return render_template("signup.html",msg=1)
        elif len(pwd)>8:
            print(len(pwd) ,"password not greater than 8 characters")
            return render_template("signup.html",msg=6)
        elif(pwd!=pwd):
            print("password miss match")
            return render_template("signup.html",msg=2)
        else:
            query="SELECT * FROM registered_users WHERE email=%s or mobile=%s"
            values=(email,mobile)
            cursor.execute(query,values)
            record = cursor.fetchone()
            
        
            if record is not None:
                print("user details:" ,record)
                print("Already exist")
                return render_template("signup.html",msg=3)
            else:
                query="INSERT INTO registered_users SET username=%s,email=%s,mobile=%s,password=%s"
                values=(username,email,mobile,pwd)
                try:
                    cursor.execute(query,values)
                    conn.commit()
                    
                    print("Successfully inserted ")
                    return render_template("login.html",msg=4)
                except Exception as e:
                    print(e)
                    return render_template("signup.html",msg=5)
                finally:
                    print("Completed")
                    cursor.close()
                    conn.close()
    

    return render_template('signup.html')


# login
@app.route("/login",methods=["GET","POST"])
def login():
    cursor,conn = dbconn()
    if session.get('uname') is not None:
        return redirect("/templatesPage")
    # elif session.get('name') is not None:
    #     return redirect("/form")
    
    user = ""
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['pwd']
        query = "SELECT * FROM registered_users WHERE (mobile = %s or email = %s) AND password = %s"
        values = (username,username,password)
        cursor.execute(query,values)
        user = cursor.fetchone()
        
        if user is not None:
            print(user)
            if user[6] == 1:
                session['id'] = user[0]
                session['name'] = user[1]
                print("success")
                return redirect("/templatesPage")
            
            else:
                print("blocked user")
                return render_template("/login.html", msg=0)
        else:
            print("not signup")
            return render_template("/login.html", msg=1)
        
    cursor.close()
    conn.close()
    return render_template("login.html") #render_template is used to call the html page





@app.route('/contactus')
def contactus():
    return render_template('contactus.html')


# log out
@app.route("/logout")
def logout():
    session.clear()   #previous values is deleted after logout the page
    return redirect("/")


# ------------- form session --------------

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/form/<int:id>", methods=["GET", "POST"])
def resume_form(id):
    print("id=",id)
    
    if request.method == "POST":
        # Collect form data
        session['uname'] = request.form.get('name')
        session['phd'] = request.form.get('phd')
        session['mtech'] = request.form.get('mtech')
        session['Dcollege'] = request.form.get('Dcollege')
        session['IDcollege'] = request.form.get('IDcollege')
        session['school'] = request.form.get('school')
        print("...............successfully read educational details...............")
        
        # Handling internships
        session['careerobj'] = request.form.get('careerobj')
        
        # Handling internships
        internship_count = int(request.form.get('internships', 0))
        print(internship_count)
        session['internships'] = []
        for i in range(1, internship_count + 1):
            internship = request.form.get('internship'+str(i))
            internship_desc = request.form.get('internshipDesc'+str(i))  # Get the achievement description
            session['internships'].append({
                'title': internship,
                'description': internship_desc
            })
            

        # Handling certifications
        certification_count = int(request.form.get('certifications', 0))
        session['certifications'] = []
        for i in range(1, certification_count + 1):
            certification = request.form.get('certification'+str(i))
            session['certifications'].append(certification)

        

        # Handling projects
        project_count = int(request.form.get('projects', 0))
        session['projects'] = []
        for i in range(1, project_count + 1):
            project = request.form.get('project'+str(i))
            project_role = request.form.get('projectrole'+str(i))
            project_desc = request.form.get('projectDesc'+str(i))  # Get the achievement description
            session['projects'].append({
                'title': project,
                'role':project_role,
                'description': project_desc
            })
            

                # Handling technical skills
        technical_skill_count = int(request.form.get('technicalSkills', 0))
        session['technical_skills'] = []
        for i in range(1, technical_skill_count + 1):
            technical_skill = request.form.get('technicalSkill' + str(i))
            session['technical_skills'].append(technical_skill)


        # Handling academic achievements in the form
        achievement_count = int(request.form.get('achievements', 0))  # Get number of achievements
        session['achievements'] = []  # Initialize session to store achievements

        for i in range(1, achievement_count + 1):
            achievement = request.form.get('achievement'+str(i))  # Get the achievement title
            achievement_desc = request.form.get('achievementDesc'+str(i))  # Get the achievement description
            session['achievements'].append({
                'title': achievement,
                'description': achievement_desc
            })


        # Experience details
        experience_count = int(request.form.get('experiences', 0))  # Get number of experiences
        session['experiences'] = []  # Initialize session to store experiences

        for i in range(1, experience_count + 1):
            experience = request.form.get('experience'+str(i))  # Get the experience title
            experience_desc = request.form.get('experienceDesc'+str(i))  # Get the experience description
            session['experiences'].append({
                'title': experience,
                'description': experience_desc
            })

        # Personal info
        session['email'] = request.form.get('email')
        session['linkedin'] = request.form.get('linkedin')
        session['contact'] = request.form.get('contact')
        session['address'] = request.form.get('address')
        session['hobbies'] = request.form.get('hobbies')
        session['strengths'] = request.form.get('strengths')
        session['weaknesses'] = request.form.get('weaknesses')
        session['fathername'] = request.form.get('Fathername')
        session['mothername'] = request.form.get('Mothername')
        session['github'] = request.form.get('github')
        session['blog'] = request.form.get('blog')
        session['gender'] = request.form.get('gender')
        session['dob'] = request.form.get('dob')
        



    

        # Handling image upload
        if 'image' in request.files:
            file = request.files['image']
            # os.makedirs(app.config['UPLOAD_FOLDER'])
            if file and allowed_file(file.filename):
                filename = file.filename
                ext = filename.rsplit(".", 1)[1]
                filename = f"{uuid.uuid4()}.{ext}"
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # path = static/uploads/sample.jpg
                file.save(path)
                session['image'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print("hello")

        # flash('Form submitted successfully!')
        if id == 1:
            print(type(id))
            return redirect("/template1")
        elif id == 2:
            print(type(id))
            return redirect("/template2")
        elif id == 3:
            return redirect("/template3")
    

    return render_template("form.html")



if __name__ == '__main__':
    app.run(debug=True)
