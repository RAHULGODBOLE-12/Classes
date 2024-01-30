"""SP_Classes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SP_Classes.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('stu_detail',stu_detail,name='stu_detail'),
    path('accounts/login/', logins, name='logins'),
    path('accounts/logout/',logout_view,name='logout'),
    path('feedback_save',feedback_save,name="feedback_save"),
    path('feedback_table',feedback_table,name="feedback_table"), 
    path('details_save',details_save,name="details_save"),
    path('edit_details/<int:id>',edit_details,name="edit_details"),
    path('update_details',update_details,name="update_details"),
    path('delete_details/<int:id>',delete_details,name="delete_details"),
    path('studetails_fileupload',studetails_fileupload,name="studetails_fileupload"),
    path('create_and_download_excel',create_and_download_excel,name="create_and_download_excel"),
    path('Stu_marks',Stu_marks,name='Stu_marks'),
    path('get_stu_name',get_stu_name,name='get_stu_name'),
    path('marks_save',marks_save,name='marks_save'),
    path('marks_edit/<int:id>',marks_edit,name="marks_edit"),
    path('marks_update',marks_update,name="marks_update"),
    path('marks_delete/<int:id>',marks_delete,name="marks_delete"),
    path('stu_result',stu_result,name='stu_result'),
    path('stu_subject_details',stu_subject_details,name='stu_subject_details'),

]
