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
    

