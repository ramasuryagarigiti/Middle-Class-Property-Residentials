import os, getpass, random
from datetime import timedelta

import mysql.connector as ms
from flask import Flask, render_template, request, session, redirect, json
from flask_mail import Message, Mail
from flask_session import Session
from validate_email import validate_email
import socket
## getting the hostname by socket.gethostname() method

## getting the IP address using socket.gethostbyname() method




app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hisir960@gmail.com'
app.config['MAIL_PASSWORD'] = 'Qwert@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1)
Session(app)


@app.before_request
def make_session_permanent():
    app.permanent_session_lifetime = timedelta(minutes=10)


@app.route("/", methods=["GET", "POST"])
def wel():
    # url = 'http://freegeoip.net/json/{}'.format(request.remote_addr)
    # r = request.get(url)
    # j = json.loads(r.text)
    # city = j['city']
    # session['city']=city
    # print(city)
    return render_template("wel.html")


@app.route("/login", methods=["GET", "POST"])
def log():
    if request.method == 'POST':
        email = request.form['eml']
        pswd1 = request.form['pswd']
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
            cu = mydb.cursor()
            # cu.execute("create database grp");
            # cu.execute("use grp");cu.execute("create table userlogin(name varchar(45), passwd varchar(25))")
            # cu.execute("select userlogin.name from userlogin where email,passwd=(%s,%s)",(email,pswd1))
            cu.execute("use rent")
            print("(from lgn)email=", email)
            cu.execute("select userlogin.eml,userlogin.passwd from userlogin where userlogin.eml=%s", (email,))
            lst = cu.fetchall()
            print("lst=", lst)
            # print("pswd1=",pswd1)
            # print("**" * 30, "Gud.")
            for i in lst:
                if i[0] == email:
                    print("i[0]=", i[0], "email=", email)
                    if i[1] == pswd1:
                        cu.execute("select userlogin.name from userlogin where userlogin.eml=%s", (email,))
                        p = cu.fetchall()
                        # cu.execute("select books.book_name,books.author,books.about from books")
                        data = cu.fetchall()
                        print("before returning i[0]=", i[0], "i[1]=", i[1])
                        cu.execute("select * from flats")
                        data = cu.fetchall()
                        # return "suc"
                        session["name"] = p[0][0]
                        if not session.get("name"):
                            return redirect("/login")

                        hostname = socket.gethostname()
                        ip_address = socket.gethostbyname(hostname)
                        session["hostip"]=ip_address
                        session["devname"]=hostname;session.permanent = True
                        return render_template("user.html", name=p[0][0],data=data,ip=session["hostip"],devnm=session["devname"])
                        # return render_template('stud.html', name=p[0][0], data=data)
                    else:
                        # print("**" * 30, "Gud.")
                        return "Incorrect Password"
                else:
                    return "user doesn't exist"
                # return render_template("home.html")

            else:
                # print("l=",lst);print("lst(frkom userlgn)=",lst);

                cu.close()
                return "Incorrect username or password!!"

        except Exception as e:
            return str(e)
        # finally:
        #     cu.close()
    # else:return "Method type: "+request.method
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def ind():
    if request.method == 'POST':
        user = request.form.get('nm')
        email = request.form.get('eml')
        pswd = request.form.get('pswd')
        # pswd2 = request.form['passwd1']
        ph = request.form.get('phn')
        rl = request.form.get('rl')
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
            cu = mydb.cursor()
            # cu.execute("create database rent");
            cu.execute("use rent")
            # cu.execute("create table signup(username varchar(50) ,email varchar(320) primary key,phone varchar(20),pswd varchar(20), role varchar(6) not null)")
            # cu.execute("create table userx(uname varchar(50),email varchar(320) primary key,phone varchar(20),pswd varchar(20))")

            lst = cu.fetchall();
            if (email.strip(),) in lst:
                return "Email already exists!!"
            # if pswd != pswd2:
            #     return "Password doesn't matches"
            else:
                # if str(validate_email(email)) == "False":
                #     return "invalid email address"
                # print("**"*30,"Gud.")
                if str(rl).lower() == "admin":
                    print("**" * 30, "Bad.")
                    cu.execute("insert into signup values(%s,%s,%s,%s,%s)",
                               (user.strip(), email.strip(), ph, pswd, rl,))
                    # cu.execute("create table admlogin(name varchar(45), eml varchar(40), passwd varchar(25), pin varchar(6))")

                    cu.execute("insert into req values(%s,%s,%s, %s)", (email.strip(),user.strip(), ph,pswd))
                    mydb.commit();cu.close()
                    # cu.execute("insert into admlogin values(%s,%s,%s,%s)", (user.strip(), email.strip(), pswd, str(pin),))
                    # mydb.commit()
                    # cu.close()
                    # sub = "House Paradox"
                    # msg = Message(
                    #     sub,
                    #     sender='hisir960@gmail.com',
                    #     recipients=[email]
                    # )
                    # msg.body = 'Hi, Thanks for registering for our website.You are a admin now.Please do not share this code with anyone your secret pin is:' + pin
                    # mail.send(msg)
                    # print("*" * 30, 'Email Sent')

                    # print(validate_email(email));
                    return "<h1 style=\" color:green\">Your request to be admin is sent to our admin.You will be able to login soon after his acceptance.</h1>"
                elif str(rl).lower() == "user":
                    cu.execute("insert into signup values(%s,%s,%s,%s,%s)",
                               (user.strip(), email.strip(), ph, pswd, rl,))
                    # cu.execute("create table userlogin(name varchar(45), eml varchar(40), passwd varchar(25))")
                    cu.execute("insert into userlogin values(%s,%s,%s)", (user.strip(), email.strip(), pswd,))
                    mydb.commit();
                    cu.close();
                    sub = "House Rental"
                    msg = Message(
                        sub,
                        sender='hisir960@gmail.com',
                        recipients=[email]
                    )
                    msg.body = 'Hi, Thanks for registering for our website.You are a user now.Thank you using our site. we are happy to have you here!!'
                    mail.send(msg)
                    print("*" * 30, 'User Email Sent')
                    return render_template("login.html")

                # print(validate_email(email));


        except Exception as e:
            if "Duplicate entry" in str(e):
                return "Email already exists!!"
            else:
                return str(e)
    return render_template("signup.html")

    # return render_template("signup.html")


@app.route("/admlgn", methods=["GET", "POST"])
def adml():
    if request.method == 'POST':
        email = request.form['eml']
        pswd1 = request.form['pswd']
        data = [
            ("01-01-2020", 1597),
            ("02-02-2020", 1456),
            ("03-03-2020", 1908),
            ("04-04-2020", 896),
            ("05-05-2020", 755),
            ("06-06-2020", 453),
            ("07-07-2020", 1100),
            ("08-08-2020", 1235),
            ("09-09-2020", 1478),
            ("10-10-2020", 1230),
            ("11-11-2020", 1540),
            ("12-12-2020", 1010),
        ]
        labels = [row[0] for row in data]
        values = [row[1] for row in data]
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@")
            cu = mydb.cursor()
            cu.execute("use rent")
            cu.execute("select admlogin.eml,admlogin.passwd from admlogin where admlogin.eml=%s", (email,))

            lst = cu.fetchall()

            # print("l=",l)
            # print("(adm)lst=", lst);print("(adm)psd=", pswd1,"==>")
            for i in lst:
                if i[0] == email:
                    if i[1] == pswd1:
                        cu.execute("select admlogin.name from admlogin where admlogin.eml=%s", (email,))
                        # print("Right na"*10)

                        m = cu.fetchall();print("M=",m);session["admname"] = m[0][0]
                        cu.execute("select * from req")
                        r=cu.fetchall()
                        if not session.get("admname"):
                            return redirect("/admlgn")
                        if session.get("admname") is not None:
                            session.permanent = True
                            cu.execute("SELECT COUNT(admlogin.name) FROM rent.admlogin");count = cu.fetchall();print("count=", count)
                            cu.execute("SELECT COUNT(flats.flat_name) FROM rent.flats");count.append(cu.fetchone());print("count=", count)
                            cu.execute("SELECT COUNT(userlogin.name) FROM rent.userlogin");count.append(cu.fetchone());print("count3=", count)
                            cu.execute("SELECT COUNT(req.eml) FROM rent.req");count.append(cu.fetchone());print("count3=", count)

                            session["count"] = count
                            return render_template('admdash.html', name=session["admname"] , req=r, labels=labels, values=values, count=session["count"])
                    else:
                        return "Incorrect Password"
                else:
                    return "user doesn't exist"

            cu.close()
        except Exception as e:
            return "Error is"+str(e)

    return render_template("admlgn.html")


@app.route("/admdash", methods=["GET", "POST"])
def dash():
    if session.get("admname") is not None:
        val = request.form.get('nm')
        data = [
            ("01-01-2020", 1597),
            ("02-02-2020", 1456),
            ("03-03-2020", 1908),
            ("04-04-2020", 896),
            ("05-05-2020", 755),
            ("06-06-2020", 453),
            ("07-07-2020", 1100),
            ("08-08-2020", 1235),
            ("09-09-2020", 1478),
            ("10-10-2020", 1230),
            ("11-11-2020", 1540),
            ("12-12-2020", 1010),
        ]
        labels = [row[0] for row in data]
        values = [row[1] for row in data]
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@")
            cu = mydb.cursor()
            cu.execute("use rent")
            cu.execute("select * from req")
            r = cu.fetchall()
            cu.execute("select * from req where req.eml=%s",(val,))
            x=cu.fetchall()
            print("req",r)
            if request.form.get('adm') == "Grant Access":
                print("In adm", val )
                print("X=",x)
                email = x[0][0]
                pin = str(random.randint(10000, 100000))
                if x:
                    cu.execute("insert into admlogin values(%s,%s,%s,%s)", (x[0][1].strip(), email.strip(), x[0][2], str(pin),))
                    cu.execute("delete from req where req.eml=%s", (email,));mydb.commit()

            elif request.form.get('adm1') == "Deny Access":
                print("Request denied", val )
                print("X=",x);email = x[0][0]
                cu.execute("delete from req where req.eml=%s", (email,))
                mydb.commit()
                cu.close()
                # sub = "House Paradox"
                # msg = Message(
                #     sub,
                #     sender='hisir960@gmail.com',
                #     recipients=[email]
                # )
                # msg.body = 'Hi, Thanks for registering for our website.You are a admin now.Please do not share this code with anyone your secret pin is:' + pin
                # mail.send(msg)
                print("*" * 30, 'Email Sent')
            return render_template("admdash.html", labels=labels, values=values, req=r, count=session["count"])

        except Exception as e:
            "Facing error is:"+str(e)
    else:
        return redirect("/admlgn")
    return render_template("admdash.html",count=session["count"])
        # return redirect(request.referrer)



@app.route("/usr", methods=["POST", "GET"])
def usr():
    if session.get("name") is not None:
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
            cu = mydb.cursor()
            cu.execute("use rent")
            cu.execute("select * from flats")
            data = cu.fetchall()
            # print("From flats from usr method:",data)
            cu.close()
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            session["hostip"] = ip_address
            session["devname"] = hostname

        except Exception as e:
            print("Error at:-"+str(e))
        return render_template("user.html", data=data, name= session["name"],ip=session["hostip"],devnm=session["devname"])
    else:return redirect("/login")

# fname = request.form['fname']
#         uname = request.form['uname']
#         ness=request.form['ness']
#         ph = request.form['phn']
#         rms=request.form['rms']
#         eml = request.form['eml']
#         rent = request.form['rent']
#         # sel=request.form['sel']
#         ademl = request.form['admeml']
#         adpin = request.form['pin']
#         pdf = request.form.get('pdf')
#         rl = request.form.get("sel")


@app.route("/addhs", methods=["POST", "GET"])
def house():
    if request.method == 'POST':
        nm = request.form['fname']
        owner = request.form['uname']
        abt = request.form['ness']
        phn = request.form['phn']
        rms = request.form['rms']
        oeml = request.form['eml']
        eml = request.form['admeml']
        pin = request.form['pin']
        rate = request.form['rent']
        pdf = request.form['pdf']
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@")
            cu = mydb.cursor()
            cu.execute("use rent")
            # cu.execute("create table flats(flat_name varchar(30), owner varchar(15),about varchar(6),owner_phone varchar(3),no_of_rooms varchar(50),owner_mail varchar(45),adm_mail varchar(45),pin varchar(4),img blob) ")
            cu.execute("select admlogin.eml,admlogin.pin from admlogin where admlogin.eml=%s", (eml,))
            lst = cu.fetchall()
            print("lst=", lst)
            for i in lst:
                if i[0] == eml:
                    if i[1] == pin:
                        cu.execute("insert into flats values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                   (nm, owner, abt, phn, rms, oeml, eml, pdf,rate))
                        mydb.commit();
                        return "<a href=\"addhs\">  <button type=\"button\" class=\"btn btn-light\">&lt; Go Back </button></a> <h2 style='color:green;'>Flat added successfully!!</h2>"
                    else:
                        return "incorrect password"
                else:
                    return "incorrect mail"

            cu.close()

            print("*" * 30)
            # print("Flat name=", nm, "pdf=", pdf)

        except Exception as e:
            print("Erroor is:", str(e))



    else:
        print("Type of method:", request.method)

    user_details = {
        'name': os.getlogin(),
        # 'email': 'john@doe.com'
    }
    name=[("Add House","Flat name","Owner of the house","Necessities nearby","Owner Phone Number","Number of room excluding bathroom","Owner email","Rent in rupees","Confirm your email","Security Pin","Flat","House"),]
    # return render_template("add.html")
    print("Name=",name)
    return render_template("add.html",user=user_details,name=name)

@app.route("/addusr", methods=["GET","POST"])
def adduser():
    if request.method == 'POST':
        user = request.form['uname']
        eml = request.form['eml']
        pswd = request.form['pswd']
        ph = request.form['phn']
        adpin = request.form['pin']
        ademl = request.form['admeml']
        rl = request.form.get('role')
        count = 0

        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
            cu = mydb.cursor()
            cu.execute("use rent")
            # cu.execute("insert into signup values(%s,%s,%s,%s,%s)", (user, email, ph, pswd, rl,))

            l = cu.execute("select admlogin.eml,admlogin.pin from admlogin where admlogin.eml=%s", (ademl,))
            lst = cu.fetchall()
            for i in lst:
                if i[0] == eml: count += 1
                if i[0] == ademl:
                    if i[1] == adpin:
                        if str(rl.lower()) == "admin" and count == 0:
                            pin = str(random.randint(1000, 10000))
                            cu.execute("insert into signup values(%s,%s,%s,%s,%s)", (user, eml, ph, pswd, rl,))
                            cu.execute("insert into admlogin values(%s,%s,%s,%s)", (user, eml, pswd, pin,))
                            mydb.commit();
                            # sub = "LMS Registration"
                            # msg = Message(
                            #     sub,
                            #     sender='hisir960@gmail.com',
                            #     recipients=[eml]
                            # )
                            # msg.body = 'Hi, Now you are registerd for our website.You are a admin now.Please do not share the below code with anyone.\n your secret pin is:' + pin
                            # mail.send(msg)
                            return "Admin added successfully!!"
                        elif str(rl.lower()) == "user":
                            cu.execute("insert into signup values(%s,%s,%s,%s,%s)", (user, eml, ph, pswd, rl,))
                            cu.execute("insert into userlogin values(%s,%s,%s)", (user, eml, pswd,))
                            mydb.commit()
                            # sub = "LMS Registration"
                            # msg = Message(
                            #     sub,
                            #     sender='hisir960@gmail.com',
                            #     recipients=[eml]
                            # )
                            # msg.body = 'Hi, Thanks for registering for our website.You are a user now.Thank you using our site. we are happy to have you here!!'
                            # mail.send(msg)

                            return "user added successfully!!"
                        else:
                            return "unable to insert user(probably because the user already exists). please try again later!!"
                    else:
                        return "incorrect Security pin"
                else:
                    return "incorrect email or email already exists"

            cu.close()
            return "Updated successfully"

        except Exception as e:
            return "error is:-" + str(e)
    user_details = {
        'name': os.getlogin(),
    }



    print("add user tye:",request.method)
    return render_template("addusr.html",user=user_details)

@app.route("/view", methods=["GET","POST"])
def vflts():
    try:
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor()
        cu.execute("use rent")
        cu.execute("select * from flats")
        data = cu.fetchall()
        print("From flatz:",data)
        return render_template("view.html", data=data, name="View Flats")

    except Exception as e:
        print("Error at:-"+e)

    return render_template("view.html")

@app.route("/viewusers")
def stds():
    try:
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor()
        cu.execute("use rent")

        cu.execute("select userlogin.name, userlogin.eml from userlogin")
        data = cu.fetchall();
        cu.close()
        hdr = ("Student", "Email",)
    except Exception as e:
        print("error:-", str(e))

    return render_template("view.html", data=data, name="View Users")


@app.route('/regflt', methods=['POST', 'GET'])
def regflts():
    if session.get("name") is not None:
        val = request.form.get('nm')
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
            cu = mydb.cursor()
            cu.execute("use rent")
            cu.execute( "select * from flats where flats.flat_name=%s",(val,))
            data = cu.fetchall()
            mydb.commit()
            cu.close()
            # print("**"*30 , "val=",val)
            # return render_template("regbk.html",data=data)
            print("type of data is:", type(data))
            # if request.method == "post":
            print("val:-",val);print("data:- ",data)
            nm1=request.form.get('nm1');print("nm1=",nm1)
            if request.form.get('submit_button') == "Confirm flat":
                print("crnm iis:", val );print("data:- ",data)
                return render_template("payment.html",amt=data[0][8],flt=data[0][0])
            return render_template("regflt.html",nm=val, data=data)
        # "select flats.flat_name,flats.owner,flats.about,flats.owner_phone,flats.rate from flats where flats.flat_name=%s",
        # (val,)
        except Exception as e:
            print("error:-(", str(e))

        return render_template("regflt.html",nm=val, data=data)
    else:
        return redirect("/login")
@app.route("/viewnew")
def view():
    try:
        mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
        cu = mydb.cursor()
        cu.execute("use rent")
        cu.execute("select * from flats ")
        data = cu.fetchall()
        mydb.commit()
        cu.close()
        return render_template("view.html", data=data, name="View Flats")
    except Exception as e:
        return str(e)

@app.route("/add", methods=['POST', 'GET'])
def adding():
    if request.method == 'POST':
        fname = request.form['fname']
        uname = request.form['uname']
        ness=request.form['ness']
        ph = request.form['phn']
        rms=request.form['rms']
        eml = request.form['eml']
        rent = request.form['rent']
        # sel=request.form['sel']
        ademl = request.form['admeml']
        adpin = request.form['pin']
        pdf = request.form.get('pdf')
        rl = request.form.get("sel")

        print("FName",fname,"UName",uname,"Ness",ness,"Owner eml",eml,"rent",rent,"rooms",rms,"ph",ph,"admeml",ademl,"adpin",adpin,"role",rl)
    else:print("Fucking GET")

    return render_template("add.html", data=[], name="Add")


@app.route('/del', methods=['POST', 'GET'])
def delt():
    return render_template("delete.html")

@app.route('/pay', methods=['POST', 'GET'])
def payt():
    if session.get("name") is not None:
        val = request.form.get('nm1')
        try:
            mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
            cu = mydb.cursor()
            cu.execute("use rent")
            cu.execute("select * from flats where flats.flat_name=%s", (val,))
            data = cu.fetchall()
            mydb.commit()
            cu.close()
            print("nm1 from pay:",val)

            return render_template("payment.html",amt=data[0][8],flt=data[0][0])
        except Exception as e:return "Error is at:"+str(e)

    else:return redirect("/login")

@app.route("/logout")
def logout():
    session["name"] = None
    session["hostip"]= None
    return redirect("/login")

@app.route("/logout1")
def logout1():
    session["admname"] = None
    session["hostip"] = None
    return redirect("/admlgn")

@app.route("/frgt", methods=['POST', 'GET'])
def frg():
    if session.get("admname") is not None:
        if request.method == "POST":
            eml = request.form.get('eml')
            try:
                mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
                cu = mydb.cursor()
                cu.execute("use rent")
                cu.execute("select admlogin.name from admlogin where admlogin.eml=%s",(eml,))
                #           select userlogin.eml from userlogin where userlogin.eml = % s", (email,)
                lst=cu.fetchall()
                print("lst=",lst)
                if list is not None:
                    print("Send email")
                    return redirect("/admdash")

            except Exception as e: print("Error from here is:" + str(e))

        else:print("Method is of type: ",request.method)
        return render_template("frgtpswd.html")
    else:
        return redirect("/admlgn")
# clicking send btn posting the info and refreshing the page automatically

