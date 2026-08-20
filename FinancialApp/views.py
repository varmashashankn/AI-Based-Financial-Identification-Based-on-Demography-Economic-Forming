from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import io
import base64
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

global username
child_schemes = ['Samagra Shiksha', 'CBSE Udaan Scholarship Scheme', 'Integrated Child Development Services']
male_schemes = ['Public Provident Fund (PPF)', 'Recurring Deposits (RD)', 'Time Deposit (TD)']
female_schemes = ['Sukanya Samriddhi Account (SSA)', 'Mahila Samriddhi Samman Patras (MSSC)']
senior_schemes = ['Senior Citizen Social Security (SCSS)', 'Postal Life Insurance (PLI)', 'Rural Postal Life Insurance (RPLI)']
dataset = pd.read_csv("Dataset/India_demography")
names = np.unique(dataset['State name']).ravel()

def PredictAction(request):
    if request.method == 'POST':
        global dataset
        name = request.POST.get('t1', False)
        population = dataset.loc[dataset['State name'] == name]
        population = population.values
        output = '<table border="1" align="center" width="100%" ><tr><th><font size="3" color="black">State Name</th>'
        output += '<th><font size="" color="black">District Name</th>'
        output += '<th><font size="" color="black">Male Population</th>'
        output += '<th><font size="" color="black">Female Population</th>'
        output += '<th><font size="" color="black">Child Population</th>'
        output += '<th><font size="" color="black">Senior Citizen Population</th>'
        output += '<th><font size="" color="black">Scheme Result</th></tr>'
        for j in range(len(population)):
            male = population[j,3]
            female = population[j,4]
            child = int(population[j,5]/1.3)
            senior =  population[j,6]
            count = np.asarray([male, female, child, senior])
            highest = np.argmax(count)
            result = ""
            if highest == 0:
                result = '<font size="3" color="blue">Male Population is high</font>'
            elif highest == 1:
                result = '<font size="3" color="black">Female Population is high</font>'
            elif highest == 2:
                result = '<font size="3" color="red">Child Population is high</font>'
            elif highest == 3:
                result = '<font size="3" color="green">Senior Citizen Population is high</font>'
            output+='<tr><td><font size="3" color="black">'+population[j,0]+'</td>'
            output+='<td><font size="3" color="black">'+population[j,1]+'</td>'    
            output+='<td><font size="3" color="black">'+str(male)+'</td>'   
            output+='<td><font size="3" color="black">'+str(female)+'</td>'
            output+='<td><font size="3" color="black">'+str(child)+'</td>'
            output+='<td><font size="3" color="black">'+str(senior)+'</td>'
            output+='<td><font size="3" color="blue">'+str(result)+'</td></tr>'
        output+="</table><br/>"
        population = dataset.loc[dataset['State name'] == name]
        population = population[['Male', 'Female', 'Child', 'Senior_Citizen']]
        population = population.values
        pop = [np.sum(population[:,0]), np.sum(population[:,1]), np.sum(population[:,2]/1.3), np.sum(population[:,3])]
        plt.pie(pop, labels=['Male', 'Female', 'Child', 'Senior_Citizen'], autopct='%.0f%%')
        plt.title(name+" State Wise Population Graph")
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        #plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.clf()
        plt.cla()
        context= {'data':output, 'img': img_b64}
        return render(request, 'UserScreen.html', context)    

def Predict(request):
    if request.method == 'GET':
        global dataset, names
        output = '<tr><td><font size="3" color="black">Choose&nbsp;State</td><td><select name="t1">'
        for i in range(len(names)):
            output += '<option value="'+names[i]+'">'+names[i]+'</option>'
        output +='</select></td></tr>'
        context= {'data1':output}
        return render(request, 'Predict.html', context)

def index(request):
    if request.method == 'GET':
        global child_schemes, male_schemes, female_schemes, senior_schemes
        output = '<table border="1" align="center" width="100%" ><tr><th><font size="3" color="black">Scheme Name</th>'
        output += '<th><font size="" color="black">Scheme For</th></tr>'
        for i in range(len(senior_schemes)):
            output+='<tr><td><font size="3" color="black">'+senior_schemes[i]+'</td>'
            output+='<td><font size="3" color="blue">Senior Citizens</td></tr>'
        for i in range(len(male_schemes)):
            output+='<tr><td><font size="3" color="black">'+male_schemes[i]+'</td>'
            output+='<td><font size="3" color="blue">Youth Scheme</td></tr>'    
        for i in range(len(female_schemes)):
            output+='<tr><td><font size="3" color="black">'+female_schemes[i]+'</td>'
            output+='<td><font size="3" color="blue">Female Scheme</td></tr>'
        for i in range(len(child_schemes)):
            output+='<tr><td><font size="3" color="black">'+child_schemes[i]+'</td>'
            output+='<td><font size="3" color="blue">Childrens Scheme</td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"    
        context= {'data':output}    
        return render(request, 'index.html', context)

def UserLogin(request):
    if request.method == 'GET':
        return render(request, 'UserLogin.html', {})

def Register(request):
    if request.method == 'GET':
        return render(request, 'Register.html', {})

def UserLoginAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'financial',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    status = 'success'
                    break
        if status == 'success':
            context= {'data':'Welcome '+username}
            return render(request, 'UserScreen.html', context)            
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)

def RegisterAction(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      contact = request.POST.get('t3', False)
      email = request.POST.get('t4', False)
      address = request.POST.get('t5', False)
      status = "none"
      con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'financial',charset='utf8')
      with con:
            cur = con.cursor()
            cur.execute("select username FROM register where username='"+username+"'")
            rows = cur.fetchall()
            if len(rows) > 0:
                status = username+" already exists"
      if status == "none":
          db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'financial',charset='utf8')
          db_cursor = db_connection.cursor()
          student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
          db_cursor.execute(student_sql_query)
          db_connection.commit()
          print(db_cursor.rowcount, "Record Inserted")
          if db_cursor.rowcount == 1:
               context= {'data':'Signup Process Completed'}
               return render(request, 'Register.html', context)
          else:
               context= {'data':'Error in signup process'}
               return render(request, 'Register.html', context)
      else:
          context= {'data': status}
          return render(request, 'Register.html', context)
