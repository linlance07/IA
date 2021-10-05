from django.shortcuts import render, redirect
from django.contrib.auth import logout
import pyrebase

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactForm



firebaseConfig = {
    'apiKey': "AIzaSyANGBWe3WlGaVRz0AlenXeL0CVB-WrTYro",
    'authDomain': "department-webapp.firebaseapp.com",
    'databaseURL': "https://department-webapp-default-rtdb.firebaseio.com",
    'projectId': "department-webapp",
    'storageBucket': "department-webapp.appspot.com",
    'messagingSenderId': "200792524960",
    'appId': "1:200792524960:web:ed6771ec8ff2bf9e86e1c5",
    'measurementId': "G-5RV1GXRFBD"
  }

firebaseConfigcse = {
    'apiKey': "AIzaSyBbp0KWKPlb7H7dJ-8je7tyeQydvzUzPYU",
    'authDomain': "department-cse-46e59.firebaseapp.com",
    'databaseURL': "https://department-cse-46e59-default-rtdb.firebaseio.com",
    'projectId': "department-cse-46e59",
    'storageBucket': "department-cse-46e59.appspot.com",
    'messagingSenderId': "130245589247",
    'appId': "1:130245589247:web:1fa1ec90a09a14c43ef4ca"  
  }

firebaseConfigeee = {
    'apiKey': "AIzaSyCQZJujBxhb-i5sPubEkG1bkSFNqLYtJZk",
    'authDomain': "department-eee-ca484.firebaseapp.com",
    'databaseURL': "https://department-eee-ca484-default-rtdb.firebaseio.com",
    'projectId': "department-eee-ca484",
    'storageBucket': "department-eee-ca484.appspot.com",
    'messagingSenderId': "396555052186",
    'appId': "1:396555052186:web:328ae5549b048965baeb23",
    'measurementId': "G-M74HL10RPZ"
  }

userx=''
users=''
count =0

fb = pyrebase.initialize_app(firebaseConfig)
db = fb.database()
store = fb.storage()
auth = fb.auth()

fbcse = pyrebase.initialize_app(firebaseConfigcse)
dbcse = fbcse.database()
storecse = fbcse.storage()

fbeee = pyrebase.initialize_app(firebaseConfigeee)
dbeee = fbeee.database()
storeeee = fbeee.storage()

def tdash(request):
    return render(request, "tdash.html")

def index(request):
    global count
    count+=1
    return render(request, "index.html",{'c':count})

def signout(request):
    
    logout(request)
    global userx
    userx=''
    return redirect('tlogin')

def ssignout(request):
    
    logout(request)
    global users
    users=''
    return redirect('slogin')



def tlogin(request):
    if request.method=='POST':
        username =request.POST["tusername"]
        password =request.POST["tpassword"]
        if password is 'cse?admin:21' or 'ece?admin:21' or 'eee?admin:21':
            try:
                userlogin= auth.sign_in_with_email_and_password(username,password)
                user = auth.refresh(userlogin['refreshToken'])    
                #print(user['userId'])
                global userx
                userx=user['userId']
                #return render(request,'tdashboard.html', {'user':user['userId']})
                return redirect('tdashboard')
            except:
                return render(request,'login.html',{'msg':'Invalid Login credentials'})
        else:
            return render(request,'login.html',{'msg':'Invalid Login credentials'})
    else:
        return render(request, "login.html")

def slogin(request):
    if request.method=='POST':
        username =request.POST["susername"]
        password =request.POST["spassword"]
        try:
            userlogin= auth.sign_in_with_email_and_password(username,password)
            #return render(request,'sdashboard.html',{'user':username})
            user = auth.refresh(userlogin['refreshToken'])   
            global users
            users=user['userId']
            return redirect('sdashboard')
        except:
            return render(request,'slogin.html',{'msg':'Invalid Login credentials'})
    return render(request, "slogin.html")

def tdashboard(request):
    #print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',userx)
    if len(userx)==0:
        return redirect('tlogin')
    if request.method=='POST':
        if 'desc' in request.POST:
            desc =request.POST["desc"]
            title =request.POST["title"]
            date =request.POST["date"]
            file = request.FILES['files[]']
            image = store.child('Achievements/'+title).get_url(None)
            ach = {'title':title, 'desc':desc,'date':date,'image':image}
            db.child('Achievements').child(title).set(ach)
            return redirect('tdashboard')
        elif 'ndesc' in request.POST:
            ndept =request.POST["ndept"]
            ndesc =request.POST["ndesc"]
            ntitle =request.POST["ntitle"]
            ndate =request.POST["ndate"]
            news = {'title':ntitle, 'desc':ndesc,'date':ndate}
            if ndept == "CSE":
                dbcse.child('News').child(ndept).child(ntitle).set(news)
            elif ndept == "EEE":
                dbeee.child('News').child(ndept).child(ntitle).set(news)
            else:
                db.child('News').child(ndept).child(ntitle).set(news)
           # print(news)
            return redirect('/tdashboard#simple2')
        else:
            if 'fname' in request.POST:
                fname =request.POST["fname"]
                dept =request.POST["dept"]
                sem =request.POST["sem"]
                sub =request.POST["sub"]
                if dept == "CSE":
                    pdfurl = storecse.child(dept+'/'+dept.lower()+'_notes'+'/'+sem+'/'+sub+'/'+fname).get_url(None)
                    dbcse.child(dept).child(sem).child(sub).child(fname).set(pdfurl)
                elif dept == "EEE":
                    pdfurl = storeeee.child(dept+'/'+dept.lower()+'_notes'+'/'+sem+'/'+sub+'/'+fname).get_url(None)
                    dbeee.child(dept).child(sem).child(sub).child(fname).set(pdfurl)
                else:
                    pdfurl = store.child(dept+'/'+dept.lower()+'_notes'+'/'+sem+'/'+sub+'/'+fname).get_url(None)
                    #print(pdfurl)
                    db.child(dept).child(sem).child(sub).child(fname).set(pdfurl)
                return redirect('/tdashboard#simple3')
            else:
                Dept =request.POST["Dept"]
                Sem =request.POST["Sem"]
                Sub =request.POST["Sub"]
                if Dept == "CSE":
                    book = dbcse.child(Dept).child(Sem).child(Sub).get().val().keys()
                elif Dept == "EEE":
                    book = dbeee.child(Dept).child(Sem).child(Sub).get().val().keys()
                else:
                    book = db.child(Dept).child(Sem).child(Sub).get().val().keys()
                #print(Dept, Sem, Sub)
                #return redirect('/tdashboard#simple3')
                return render(request, "tdashboard.html", {'book':list(book), 'DEPT':Dept, 'SEM':Sem, 'SUB':Sub, 'A':'active'})
    else:
        ach =  db.child('Achievements').get().val()
        achdic={}
        for i in ach.keys():
            achdic[i] = list(ach[i].values())
        cse_news = dbcse.child('News').child('CSE').get().val()
        ece_news = db.child('News').child('ECE').get().val()
        eee_news = dbeee.child('News').child('EEE').get().val()
        csedic = {}
        for j in cse_news.keys():
            csedic[j] = list(cse_news[j].values())

        ecedic = {}
        for j in ece_news.keys():
            ecedic[j] = list(ece_news[j].values())

        eeedic = {}
        for j in eee_news.keys():
            eeedic[j] = list(eee_news[j].values())
        return render(request,'tdashboard.html',{'achdic':achdic, 'csedic':csedic, 'ecedic':ecedic, 'eeedic':eeedic})

def cse_home(request):
    return render(request, "cse.html")


def sdashboard(request):
    if len(users)==0:
        return redirect('slogin')
    return render(request, "sdashboard.html")

def cse_news(request):
    news =  dbcse.child('News').child('CSE').get().val()
    newsdic={}
    for i in news.keys():
        newsdic[i] = list(news[i].values())
    return render(request, "cse_news.html",{'newsdic': newsdic})


def ece_news(request):
    news =  db.child('News').child('ECE').get().val()
    newsdic={}
    for i in news.keys():
        newsdic[i] = list(news[i].values())
    return render(request, "ece_news.html",{'newsdic': newsdic})


def eee_news(request):
    news =  dbeee.child('News').child('EEE').get().val()
    newsdic={}
    for i in news.keys():
        newsdic[i] = list(news[i].values())
    return render(request, "eee_news.html",{'newsdic': newsdic})


def temp(request):
    return render(request, "temp.html")

def reg(request):
    if request.method=='POST':
        username =request.POST["susername"]
        password =request.POST["spassword"]
        rpassword =request.POST["srpassword"]

        try:
            if  password==rpassword:
                user = auth.create_user_with_email_and_password(username,password)
                return redirect("slogin")
    
            else:
                return HttpResponse('Retype the correct password')
            
        except:
            #print('Invalid email or password too short')
            pass
    
    return render(request, "reg.html")

def eee_home(request):
    return render(request, "eee.html")

def cse_syllabus(request):
    return render(request, "cse_syllabus.html")

def eee_syllabus(request):
    return render(request, "eee_syllabus.html")

def contact(request):
    return render(request, "contact.html")

def uploadnotes(request):
    if request.method=='POST':
        if 'fname' in request.POST:
            fname =request.POST["fname"]
            dept =request.POST["dept"]
            sem =request.POST["sem"]
            sub =request.POST["sub"]
            pdfurl = store.child(dept+'/'+dept.lower()+'_notes'+'/'+sem+'/'+sub+'/'+fname).get_url(None)
            #print(pdfurl)
            db.child(dept).child(sem).child(sub).child(fname).set(pdfurl)
            return redirect('uploadnotes')
        else:
            Dept =request.POST["Dept"]
            Sem =request.POST["Sem"]
            Sub =request.POST["Sub"]
            book = db.child(Dept).child(Sem).child(Sub).get().val().keys()
            #print(Dept, Sem, Sub)
            
            return render(request, "uploadnotes.html", {'book':list(book), 'DEPT':Dept, 'SEM':Sem, 'SUB':Sub})

    else:
        return render(request, "uploadnotes.html")

def cse_cgpa(request):
    sem_dict = {1:{'Communicative English':4 ,'Engineering Mathematics I':4, 'Engineering Physics':3, 'Engineering Chemistry':3, 'Problem Solving and Python Programming':3, 'Engineering Graphics':4, 'Problem Solving and Python Programming Laboratory':2, 'Physics and Chemistry Laboratory':2},
                2:{'Technical English':4, 'Engeneering Mathematics II':4, 'Physics for information Science':3, 'BEEE':3, 'EVS':3, 'Programming in C':3, 'Engineering Practices Lab':2, 'C Lab':2},
                3:{'Discrete Mathematics':4,'Digital Principles and System Design':4, 'Data Structures':3, 'Object Oriented Programming':3, 'Communication Engineering':3, 'Data Structures Laboratory':2, 'Object Oriented Programming Laboratory':2, 'Digital Systems Laboratory':2, 'Interpersonal Skills/Listening & Speaking':1},
                4:{'Probability and Queueing Theory':4,'Computer Architecture':3, 'Database Management Systems':3, 'Design and Analysis of Algorithms':3, 'Operating Systems':3, 'Software Engineering':3, 'Database Management Systems Laboratory':2, 'Operating Systems Laboratory':2, 'Advanced Reading and Writing':1},
                5:{'Algebra and Number Theory':4,'Computer Networks':3, 'Microprocessors and Microcontrollers ':3, 'Theory of Computation':3, 'Object Oriented Analysis and Design':3, 'Open Elective I ':3, 'Microprocessors and Microcontrollers Laboratory':2, 'Object Oriented Analysis and Design Laboratory':2, 'Networks Laboratory':2},
                6:{'Internet Programming':3,'Artificial Intelligence':3, 'Mobile Computing  ':3, 'Compiler Design':4, 'Distributed Systems':3, 'Professional Elective I ':3, 'Internet Programming Laboratory':2, 'Mobile Application Development Laboratory':2, 'Mini Project':1,'Professional Communication':1},
                7:{'Principles of Management':3,'Cryptography and Network Security ':3, 'Cloud Computing':3, 'Open Elective II':3, 'Professional Elective II':3, 'Professional Elective III ':3, 'Cloud Computing Laboratory':2, 'Security Laboratory ':2},
                8:{'Professional Elective IV':3, 'Professional Elective V ':3, 'Project Work':10}
                }
    if request.method == "POST":
        
        if 'sem' in request.POST:
            sem = int(request.POST["sem"])
            return render(request, "cse_cgpa.html", {'semm':list(sem_dict[sem].keys()), 'sem_no':sem})
        else:
            sem1 = int(request.POST["semno"])
            sum_res = 0
            for i,j in sem_dict[sem1].items():
                x = int(request.POST[i])   
                sum_res = sum_res + (x*j)
            ans = sum_res/sum(sem_dict[sem1].values())
            return render(request, "cse_cgpa.html", {'semm':list(sem_dict[sem1].keys()), 'sem_no':sem1, 'ans':ans})
    else:
        return render(request, "cse_cgpa.html", {'semm':list(sem_dict[1].keys()), 'sem_no':1})
        
def eee_cgpa(request):
    sem_dict = {1:{'Communicative English':4 ,'Engineering Mathematics I':4, 'Engineering Physics':3, 'Engineering Chemistry':3, 'PSPP':3, 'Engineering Graphics':4, 'PSPP Lab':2, 'Physics and Chemistry Lab':2},
                2:{'Technical English':4, 'Engeneering Mathematics II':4,'Basic Civil and Mechanical Engineering ':4, 'Physics for electronics engineering':3, 'Circuit Theory':3, 'Environmental Science and Engineering':3, 'Engineering Practices Laboratory':2, 'Electric Circuits Laboratory ':2},
                3:{'Discrete Mathematics':4,'Digital Logic Circuits':3, 'Electromagnetic Theory':3, 'Electrical Machines - I ':3, 'Electron Devices and Circuits ':3,'Power Plant Engineering':3, 'Electronics Laboratory':2, 'Electrical Machines Laboratory - I':2},
                4:{'Numerical Methods ':4,'Control Systems ':4,'Electrical Machines - II ':3, 'Transmission and Distribution ':3, 'Measurements and Instrumentation ':3, 'Linear Integrated Circuits and Applications ':3, 'Electrical Machines Laboratory - II':2, 'Linear and Digital Integrated Circuits Laboratory':2, 'Technical Seminar':1},
                5:{'Power System Analysis':3,'Microprocessors and Microcontrollers':3, 'Power Electronics  ':3, 'Digital Signal Processing ':3, 'Object Oriented Programming':3, 'Open Elective I ':3, 'Control and Instrumentation Laboratory':2, 'Object Oriented Programming Laboratory':2, 'Professional Communication':1},
                6:{'Solid State Drives ':3,'Protection and Switchgear':3, 'Embedded Systems':3,'Professional Elective I ':3, 'Professional Elective II ':3, 'Power Electronics and Drives Laboratory':2, 'Microprocessors and Microcontrollers Laboratory':2, 'Mini Project':2},
                7:{'High Voltage Engineering':3,'Power System Operation and Control  ':3, 'Renewable Energy Systems ':3, 'Open Elective II':3, 'Professional Elective III':3, 'Professional Elective IV ':3, 'Power System Simulation Laboratory':2, 'Renewable Energy Systems Laboratory':2},
                8:{'Professional Elective V':3, 'Professional Elective VI ':3, 'Project Work':10}
                }
    if request.method == "POST":
        
        if 'sem' in request.POST:
            sem = int(request.POST["sem"])
            return render(request, "cse_cgpa.html", {'semm':list(sem_dict[sem].keys()), 'sem_no':sem})
        else:
            sem1 = int(request.POST["semno"])
            sum_res = 0
            for i,j in sem_dict[sem1].items():
                x = int(request.POST[i])   
                sum_res = sum_res + (x*j)
            ans = sum_res/sum(sem_dict[sem1].values())
            return render(request, "cse_cgpa.html", {'semm':list(sem_dict[sem1].keys()), 'sem_no':sem1, 'ans':ans})
    else:
        return render(request, "eee_cgpa.html", {'semm':list(sem_dict[1].keys()), 'sem_no':1})
        


    
def packages(request):
    return render(request, "packages.html")


def achievements(request):
    ach =  db.child('Achievements').get().val()
    achdic={}
    for i in ach.keys():
        achdic[i] = list(ach[i].values())
    #print(achdic)
    return render(request, "achievements.html",{'achdic': achdic})

def notes(request):
    x= dbcse.child("CSE").child('Sem4').child('PRP').get().val()
    return render(request, "notes.html",{'key':x})

def eee_notes(request):
    x= dbeee.child('EEE').child('Sem4').child('EC2').get().val()
    return render(request, "eee_notes.html",{'key':x})

def contact(request):
    return render(request, "contact.html")

def ece_home(request):
    return render(request, "ece.html")

def ece_syllabus(request):
    return render(request, "ece_syllabus.html")

def ece_cgpa(request):
    sem_dict = {1:{'Communicative English':4 ,'Engineering Mathematics I':4, 'Engineering Physics':3, 'Engineering Chemistry':3, 'Problem Solving and Python Programming':3, 'Engineering Graphics':4, 'Problem Solving and Python Programming Laboratory':2, 'Physics and Chemistry Laboratory':2},
                2:{'Technical English':4, 'Engeneering Mathematics II':4, 'Physics for Electronics Engineering':3, 'Basic Electrical and Instrumentation Engineerong':3, 'Circuit Analysis':4, 'Electronic Devices':3, 'Engineering Practices Laboratory':2, 'Circuits and Devices Laboratory':2},
                3:{'Linear Algebra and Partial Differential Equations':4,'Fundamentals of Data Structures in C':3, 'Electronic Ciruits I':3, 'Signals and Systems':4, 'Digital Electronics':3, 'Control Systems Engineering':3, 'Fundamentals of Data Structures in C laboratory':2, 'Analog and Digital Ciruits Laboratory':2, 'Interpersonal Skills/Listening & Speaking':1},
                4:{'Probability and Random Processes':4,'Electronic Circuits II':3, 'Communication Theory':3, 'Electromagnetic Fields':4, 'Linear Integrated Circuits':3, 'Environmental Science and Engineering':3, 'Circuits Design and Simulation Laboratory':2, 'Linear Integrated circuits Laboratory':2},
                5:{'Digital Communication':3,'Discrete-Time Signal Processing':4, 'Computer Architecture and Organization':3, 'Communication Networks':3, 'Professional Elective I':3, 'Open Elective I ':3, 'Digital Signal Processing Laboratory':2, 'Communication Systems Laboratory':2, 'Communication Networks Laboratory':2},
                6:{'Microprocessors and Microcontrollers':3,'VLSI Design':3, 'Wireless Communication':3, 'Principles of Management':3, 'Transmission Lines and RF Systems':3, 'Professional Elective II ':3, 'Microprocessors and Microcontrollers Laboratory':2, 'VLSI Design Laboratory':2, 'Technical Seminar':1,'Professional Communication':1},
                7:{'Antennas and Microwave Engineering':3,'Optical Communication':3, 'Embedded and Real Time Systems':3, 'Ad hoc and Wireless Sensor Networks':3, 'Professional Elective III':3, 'Open Elective II ':3, 'Embedded Laboratory':2, 'Advanced Communication Laboratory':2},
                8:{'Professional Elective IV':3, 'Professional Elective V':3, 'Project Work':10}
                }
    if request.method == "POST":
        
        if 'sem' in request.POST:
            sem = int(request.POST["sem"])
            return render(request, "ece_cgpa.html", {'semm':list(sem_dict[sem].keys()), 'sem_no':sem})
        else:
            sem1 = int(request.POST["semno"])
            sum_res = 0
            for i,j in sem_dict[sem1].items():
                x = int(request.POST[i])   
                sum_res = sum_res + (x*j)
            ans = sum_res/sum(sem_dict[sem1].values())
            
            return render(request, "ece_cgpa.html", {'semm':list(sem_dict[sem1].keys()), 'sem_no':sem1, 'ans':ans})
    else:
        return render(request, "ece_cgpa.html", {'semm':list(sem_dict[1].keys()), 'sem_no':1})

def ece_notes(request):
    x= db.child('Semester3').get().val()
    prp = db.child('ECE').child('Sem4').child('PRP').get().val()
    evs = db.child('ECE').child('Sem4').child('EVS').get().val()
    lic = db.child('ECE').child('Sem4').child('LIC').get().val()
    ct = db.child('ECE').child('Sem4').child('CT').get().val()
    ec2 = db.child('ECE').child('Sem4').child('EC2').get().val()
    emf = db.child('ECE').child('Sem4').child('EMF').get().val()
    return render(request, "ece_notes.html",{'key':x, 'sem4prp':prp, 'sem4evs':evs, 'sem4lic':lic, 'sem4ct':ct, 'sem4ec2':ec2, 'sem4emf':emf})