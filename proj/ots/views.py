from django.shortcuts import render
from django.urls import path,include
from django.contrib import admin
from django.http import HttpResponse,HttpResponseRedirect
from ots.models import*
from proj import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail
import random
def welcome(request):
    return render(request,'index.html')
def CandidateRegistrationForm(request):
    return render(request, 'registration_form.html')
def CandidateRegistration(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['pass1']
        email=request.POST['email']
        if(username==""  or (request.POST['pass1']=="" or request.POST['name']=="")):
          userStatus=0
        elif(len(Candidate.objects.filter(username=username))):
            userStatus=1
        elif(request.POST['pass1']!=request.POST['pass2']):
            userStatus=4            
        else:
            candidate=Candidate()
            candidate.username=username
            candidate.password=request.POST['pass1']
            candidate.name=request.POST['name']
            candidate.save()
            my_user=User.objects.create_user(username,email,password)
            my_user.save()
            userStatus=2
    else:
        userStatus=3
    context={
       'userStatus':userStatus
    }
    return render(request,'registration.html',context)


def loginView(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        candidate=Candidate.objects.filter(username=username,password=password)
        if(len(candidate)==0):
            loginError="Invalid Username or Password"
            res=render(request,'login.html',{'loginError':loginError})
        else:
            #login succesful#
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name
            res=HttpResponseRedirect("home")
    else:
       res=render(request,'login.html')
    return res
def CandidateHome(request):
    if 'name' not in request.session.keys():
        res= HttpResponseRedirect("login")
    else:
        return render(request,"home.html")

def testPaper(request):
   if 'name' not in request.session.keys():
       res= HttpResponseRedirect("login")
   n=int(request.GET['n'])
   question_pool=list(Question.objects.all())
   random.shuffle(question_pool)
   questions_list=question_pool[:n]
   context={'questions':questions_list}
   res= render(request,"test_paper.html",context)
   return res
def CalculateTestResult(request):
    if 'name' not in request.session.keys():
        res= HttpResponseRedirect("login")
    total_attempt=0
    total_right=0
    total_wrong=0
    qid_list=[]
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question=Question.objects.get(q_id=n)
        try:
            if question.ans==request.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:
            pass
    points=(total_right-total_wrong)/len(qid_list)*10
    result=Result()
    result.username=Candidate.objects.get(username=request.session['username'])
    result.attempt=total_attempt
    result.right=total_right
    result.wrong=total_wrong
    result.points=points
    result.save()
    #update candidate table#
    candidate=Candidate.objects.get(username=request.session['username'])
    candidate.test_attempted+=1
    candidate.points=(candidate.points*(candidate.test_attempted-1)+points)/candidate.test_attempted
    candidate.save()
    return HttpResponseRedirect('result')
def  testResultHistory(request):
    if 'name' not in request.session.keys():
        res= HttpResponseRedirect("login")
    candidate=Candidate.objects.filter(username=request.session['username'])
    results=Result.objects.filter(username_id=candidate[0].username)
    context={
        'candidate':candidate[0],'results':results
    }
    res=render(request,'candidate_history.html',context)
    return res
def showTestResult(request):
    if 'name' not in request.session.keys():
        res= HttpResponseRedirect("login")
    result=Result.objects.filter(resultid=Result.objects.latest('resultid').resultid,username_id=request.session['username'])
    context={
        'results':result
    }
    res=render(request,'show_result.html',context)
    return res
def logoutView(request):
    if 'name' in request.session.keys():
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect("login")
# Create your views here.
