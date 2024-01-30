from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseServerError,response,JsonResponse)
from django.contrib.auth.models import User,Group
from .forms import UserLoginForm
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from SP_Classes.forms import *
import logging
from SP_Classes.models import *
import pandas as pd
import openpyxl
from tkinter import messagebox
from flask import Flask, send_file
from io import BytesIO
from django.contrib.auth.hashers import make_password


def home(request):
    # if request.user.is_superuser:
    #     data1 = feedbacks.objects.all().order_by('-id')
    #     return render(request,"feedback.html",{'data2':data1})
    # else:
        return render(request,'index.html')

def logins(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if request.POST and form.is_valid()!=True:
        messages.error(request, 'Please check the username and Password')
    if form.is_valid():
        print(request.user)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if request.user.is_authenticated :
            if next:
                return redirect(next)
        return redirect('home')
    elif request.user.is_authenticated:
        if next:
            return redirect(next)
        return redirect('home' )
    return render(request,'accounts/user_login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def csrf_failure(request, reason=""):
    return redirect('/')

@login_required
def login_via_admin(request,id):
    if request.user.is_superuser:
        user=User.objects.get(id=id)
        login(request, user)
        return redirect('/')
    else:
        return redirect('/')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/changepassword.html', {'form': form})

def feedback_save(request):
    if request.method == "POST":
        x = feedbacks(Name = request.POST.get("yourname"),
                    Email = request.POST.get("youremail"),
                    Mobil_no = request.POST.get("yourmobileno"),
                    Comments = request.POST.get("comments"))
    x.save() 
    return redirect("/") 

def feedback_table(request):
    data1 = feedbacks.objects.all().order_by('-id')
    return render(request,"feedback.html",{'data2':data1})

def stu_detail(request):
    detail9 = Add_details.objects.filter(Class = 'IX').order_by('-Name')
    detail10 = Add_details.objects.filter(Class = 'X').order_by('-Name')
    detail11 = Add_details.objects.filter(Class = 'XI').order_by('-Name')
    detail12 = Add_details.objects.filter(Class = 'XII').order_by('-Name')
    
    return render(request,"add_details.html",{'data10':detail9,'data11':detail10,'data12':detail11,'data13':detail12})

def details_save(request):
    if request.method == "POST":
        x = Add_details(Name=request.POST.get("stuname"),
                    Class=request.POST.get("stuclass"),
                    School=request.POST.get("stuschool"),
                    DOB=request.POST.get("dob"),
                    Age=request.POST.get("age"),
                    Subject=','.join(request.POST.getlist("stusubject")),
                    Father_name=request.POST.get("father_name"),
                    Mother_name=request.POST.get("mother_name"),
                    Phone_no=request.POST.get("phone_no"),
                    Father_phno=request.POST.get("father_no"),
                    Address=request.POST.get("address"))
        x.save()
        User(username=request.POST.get("stuname"),password = make_password('iness123')).save()
        
        
        messages.success(request, 'Your Details Saved Successfully')
        if request.user.is_superuser:
            return redirect("/stu_detail")
        else:
            return render(request,'index.html')
            
    
def edit_details(request,id):
    y = Add_details.objects.filter(id=id).values()
    return JsonResponse({'data':list(y)},safe=False )

def update_details(request):
    id=request.POST.get('editid')
    print(id,'id')
    y = Add_details.objects.filter(id=id).update(Name=request.POST.get("stuname"),
                    Class=request.POST.get("stuclass"),
                    School=request.POST.get("stuschool"),
                    DOB=request.POST.get("dob"),
                    Age=request.POST.get("age"),
                    Subject=','.join(request.POST.getlist("stusubject")),
                    Father_name=request.POST.get("father_name"),
                    Mother_name=request.POST.get("mother_name"),
                    Phone_no=request.POST.get("phone_no"),
                    Father_phno=request.POST.get("father_no"),
                    Address=request.POST.get("address"))
    # return render(request,"bom/edit_bom.html",{"Add_Details":y})
    return redirect("/stu_detail")


def delete_details(request,id):
    y = Add_details.objects.get(id=id)
    y.delete()
    return redirect("/stu_detail")

def studetails_fileupload(request):
    mess=request.FILES['upload_file']
    data = pd.read_excel(mess)
    data.fillna(' ', inplace=True)
    row_iter = data.iterrows()
    
    for index, row in row_iter:
        print(row['Name'],'name')
        if Add_details.objects.filter(Name=row['Name'],Phone_no=row['Phone No'],DOB=row['DOB']).exists():
            pass
        else:     
            datas=Add_details(
                Name= row['Name'],
                Class = row['Class'],
                School = row['School'],
                DOB = row['DOB'],
                Age = row['Age'],
                Subject = row['Subject'],
                Father_name = row['Father Name'],
                Mother_name = row['Mother Name'],
                Phone_no = row['Phone No'],
                Father_phno = row['Father No'],
                Address = row['Address'],
                
                
                
            )
            datas.save()       
            
    # messages.success(request, "Data uploaded Successfully!")

    return redirect('/stu_detail')

# def messagebox_excel(request):
#     xcel_file_path = 'path/to/your/excel/template.xlsx'
#     workbook = openpyxl.load_workbook(excel_file_path)

def create_and_download_excel(request):
    print('in vies')
    headers = ['Expense ID', 'Partner Requestor', 'Ciena Planner', 'Partner Request ID', 'Type', 'Expense Type', 'Priority', 'Root Cause', 'Product Line', 'Impacted Parts', 'Supplier Name', 'Manufacturer Name', 'Qty Secured', 'Quote Price', 'Fees Total', 'Ciena current Fiscal qtr', 'Forecasted Claim Month', 'Justification Notes', 'Ciena PPV Approval Status Update', 'PPV Approval Comments', 'Ciena Internal Comments']
    ppv_data = pd.DataFrame(columns=headers)
    print(ppv_data,'dataframe')

    with BytesIO() as b:
        with pd.ExcelWriter(b) as writer:
            ppv_data.to_excel(writer, index=False, sheet_name="Sheet1")
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            writer.close()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'inline; filename="Download Excel.xlsx"'
            return response
    

def Stu_marks(request):
    detail9 = Add_marks.objects.filter(Class = 'IX').order_by('-Name')
    detail10 = Add_marks.objects.filter(Class = 'X').order_by('-Name')
    detail11 = Add_marks.objects.filter(Class = 'XI').order_by('-Name')
    detail12 = Add_marks.objects.filter(Class = 'XII').order_by('-Name')
    return render(request,"add_marks.html",{'data10':detail9,'data11':detail10,'data12':detail11,'data13':detail12})


def get_stu_name(request):
    Class = request.POST.get('get_class')
    print(Class,'Class')
    stu_name = Add_details.objects.filter(Class=Class).values_list('Name',flat=True)
    print(stu_name)
    
    return JsonResponse(list(stu_name),safe=False)

def marks_save(request):
    if request.method == "POST":
        a = Add_marks(Class = request.POST.get("stuclass"),Name = request.POST.get("stuname"),
                      RollNo = request.POST.get("rollno"),English = request.POST.get("english"),
                      Tamil = request.POST.get("tamil"),Maths = request.POST.get("maths"),
                      Science = request.POST.get("science"),Social = request.POST.get("social"),
                      Physics = request.POST.get("physics"),Chemistry = request.POST.get("social"),
                      Biology = request.POST.get("social"),Computer_Science = request.POST.get("social"),
                      All = request.POST.get("social"))
        a.save()
    return redirect('/Stu_marks')

def marks_edit(request,id):
    y = Add_marks.objects.filter(id=id).values()
    return JsonResponse({'data':list(y)},safe=False )

def marks_update(request):
    id=request.POST.get('editid')
    print(id,'id')
    y = Add_marks.objects.filter(id=id).update(Class = request.POST.get("stuclass"),Name = request.POST.get("stuname"),
                      RollNo = request.POST.get("rollno"),English = request.POST.get("english"),
                      Tamil = request.POST.get("tamil"),Maths = request.POST.get("maths"),
                      Science = request.POST.get("science"),Social = request.POST.get("social"))
    return redirect("/Stu_marks")
def marks_delete(request,id):
    y = Add_marks.objects.get(id=id)
    y.delete()
    return redirect("/Stu_marks")

def stu_result(request):
    get_student = Add_details.objects.filter(Name = request.user.username)[:1].get()
    print(get_student.Class)
    data = Add_marks.objects.filter(Name = request.user.username).order_by('-Name')
    return render(request,"result.html",{'data10':get_student,'data11':get_student,'data12':get_student,'data13':get_student,'result':data})

def stu_subject_details(request):
    Stu_name = request.POST.get('get_name')
    Stu_Class = request.POST.get('get_class')
    print(Stu_name,'name')
    print(Stu_Class,'Class')
    stu_subject = Add_details.objects.filter(Class=Stu_Class,Name=Stu_name).values_list('Subject',flat=True)
    
    for i in stu_subject:
        subjects=i.split(',')
    return JsonResponse(subjects,safe=False)