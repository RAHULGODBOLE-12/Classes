from django.db import models

class feedbacks(models.Model):
    Name = models.CharField(max_length = 100 ,null = True)
    Email = models.CharField(max_length = 100 ,null = True)
    Mobil_no = models.CharField(max_length = 100 ,null = True)
    Comments = models.CharField(max_length = 100 ,null = True)

class Add_details(models.Model):
    Name = models.CharField(max_length = 100 ,null = True)
    Class = models.CharField(max_length = 100 ,null = True)
    School = models.CharField(max_length = 100 ,null = True)
    DOB = models.CharField(max_length = 100 ,null = True)
    Age = models.CharField(max_length = 100 ,null = True)
    Father_name = models.CharField(max_length = 100 ,null = True)
    Mother_name = models.CharField(max_length = 100 ,null = True)
    Address = models.CharField(max_length = 100 ,null = True)
    Phone_no = models.CharField(max_length = 100 ,null = True)
    Father_phno = models.CharField(max_length = 100 ,null = True)
    Subject = models.CharField(max_length = 100 ,null = True)
    
class Add_marks(models.Model):
    Class = models.CharField(max_length = 100 ,null = True)
    Name = models.CharField(max_length = 255 ,null = True)
    RollNo = models.CharField(max_length = 1000 ,null = True)
    All = models.CharField(max_length = 100 ,null = True)
    English = models.CharField(max_length = 100 ,null = True)
    Tamil = models.CharField(max_length = 100 ,null = True)
    Maths = models.CharField(max_length = 100 ,null = True)
    Science = models.CharField(max_length = 100 ,null = True)
    Social = models.CharField(max_length = 100 ,null = True)
    Physics = models.CharField(max_length = 100 ,null = True)
    Chemistry = models.CharField(max_length = 100 ,null = True)
    Biology = models.CharField(max_length = 100 ,null = True)
    Computer_Science = models.CharField(max_length = 100 ,null = True)