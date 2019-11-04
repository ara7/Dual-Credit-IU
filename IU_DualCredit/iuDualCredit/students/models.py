from django.db import models
from datetime import datetime
from courses.models import ClassData

# Create your models here.
class Student(models.Model):

  University_ID	= models.IntegerField(default=0)	
  Appl_Nbr	= models.IntegerField(default=0)	
  Effective_Date	= models.DateField(default=datetime.now, blank=True)
  Academic_Plan_Code	= models.CharField(max_length = 200)
  Academic_Program_Code	= models.CharField(max_length = 200)
  Institution_Code	= models.CharField(max_length = 200) 
  First_Name = models.CharField(max_length = 200) 
  Last_Name	= models.CharField(max_length = 200) 
  Middle_Name	= models.CharField(max_length = 200)
  Other_Email_Address	= models.CharField(max_length = 200)
  GDS_Campus_Email_Address = models.CharField(max_length = 200)
  Network_ID = models.CharField(max_length = 200)