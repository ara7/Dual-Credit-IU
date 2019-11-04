from django.db import models
from datetime import datetime
from enrollments.models import Enrollments, GrantEnrollmentData

# Create your models here.
class ClassData(models.Model):
  CLS_NBR = models.IntegerField()	
  
  CRS_ID =  models.IntegerField()
  ACAD_TERM_CD = models.IntegerField()

  #enrollment = models.ManyToManyField(Enrollments)
  #grantEnrollment = models.ManyToManyField(GrantEnrollmentData)

  CLS_INSTR_NM = models.TextField(blank=True)
  CLS_INSTR_GDS_CMP_EMAIL_ADDR = models.TextField(blank=True)
  CAMPUS = models.CharField(max_length=200)
  ENROLLMENT_CAP = models.IntegerField()
  ENROLLMENT_TOTAL = models.IntegerField()
  
  #Details Field

class Meta:
    ordering = ['-id']