from django.db import models
from datetime import datetime

# Create your models here.
class Enrollments(models.Model):
    CLS_NBR	= models.IntegerField(default=0)
    PRSN_UNIV_ID = models.IntegerField(default=0)
    INST_CD	= models.CharField(max_length = 20)
    ACAD_TERM_CD = models.IntegerField(default=0)
    CRS_OFCL_GRD_CD	= models.CharField(max_length = 200)
    STU_ENRL_ADD_DT = models.DateField(default=datetime.now, blank=True)
    STU_ENRL_DRP_DT = models.DateTimeField(default=datetime.now, blank=True)
    CRS_ID = models.IntegerField(default=0)
    CRS_DESC = models.CharField(max_length = 200)
    CRS_SUBJ_CD	= models.CharField(max_length = 200)
    CRS_CATLG_NBR = models.IntegerField(default=0)
    CLS_INSTR_NM = models.CharField(max_length = 200)
    CLS_INSTR_GDS_CMP_EMAIL_ADDR = models.CharField(max_length = 200)
    CMP_LOC_CD	= models.CharField(max_length = 30)
    STU_WTHD_DESC = models.CharField(max_length = 500)
    STU_WTHD_REAS_DESC = models.CharField(max_length = 500)

class GrantEnrollmentData(models.Model):
    CLS_NBR = models.IntegerField(default=0)
    COURSE_SUBJECT_Code = models.CharField(max_length = 500)
    PRSN_UNIV_ID = models.IntegerField(default=0)
    ACAD_TERM_CD = models.IntegerField(default=0)
    GRANT_ID = models.IntegerField(default=0)

class Meta:
    ordering = ['-id']