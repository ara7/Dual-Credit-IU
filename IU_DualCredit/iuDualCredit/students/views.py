from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Student, ClassData
from django.db import connection
from django.http import JsonResponse
from DAL import studentsDAL
from DAL import coursesDAL 
from DAL import enrollmentsDAL 
import csv
from helpers import logging
import sys
from datetime import datetime

# Create your views here.
def index(request):
    
    try:

        campusList = coursesDAL.campusOfEnrollmentList()
        dcPartnerList = studentsDAL.dcPartnerList()

        context = {
        'campuses' : campusList,
        'dcPartners' : dcPartnerList
        }
    
    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return render(request, 'students/search.html', context)



def studentSearch(request):
   
    try:
        
        username = request.GET.get('username', None)
        uid = request.GET.get('uid', None)
        firstname = request.GET.get('firstname', None)
        lastname = request.GET.get('lastname', None)
        campusOfenrollment = request.GET.get('campusOfenrollment', None)
        studentType = request.GET.get('studentType', None)
        dcPartner = request.GET.get('dcPartner', None)
        currentlyEnrolled = request.GET.get('currentlyEnrolled', None)
        # pendingEnrollmentReq = request.GET.get('pendingEnrollmentReq', None)

        campusList = coursesDAL.campusOfEnrollmentList()
        dcPartnerList = studentsDAL.dcPartnerList()

        studentsList = studentsDAL.studentsList(username, uid, firstname, lastname, campusOfenrollment, dcPartner, currentlyEnrolled)

        context = {
            'campuses' : campusList,
            'dcPartners' : dcPartnerList,
            'studentDetails': studentsList
        }

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return JsonResponse(context)


def studentDetailView(request, student_uid):

    try:

        StudentDetailList, StudentFormerNamesList, studentQualitricsTabHeaderList, studentEnrollmentHistoryList, StudentCourseRequest = studentsDAL.studentDetailView(str(student_uid))

        studentDetailsDict = {}
        if StudentDetailList:
            studentDetailsDict['Student Name'] = StudentDetailList[0]
            studentDetailsDict['User Name'] = StudentDetailList[1]
            studentDetailsDict['UID'] = StudentDetailList[2]
            studentDetailsDict['Date of Birth'] = StudentDetailList[3]
            # studentDetailsDict['Citizenship'] = 'None'
            # studentDetailsDict['Student Type'] = 'None'

            studentDetailsDict['Legal Sex'] = StudentDetailList[4]
            studentDetailsDict['Gender Identity'] = StudentDetailList[5]
            studentDetailsDict['Phone Number'] = StudentDetailList[6]
            studentDetailsDict['Contact Method'] = StudentDetailList[7]
            studentDetailsDict['Email'] = StudentDetailList[8]

            studentDetailsDict['Current Mailing Address'] = StudentDetailList[9]
            studentDetailsDict['Permanent Mailing Address'] = StudentDetailList[10]
            studentDetailsDict['Residency'] = StudentDetailList[11]
            studentDetailsDict['Documents Send under another name'] = StudentDetailList[12]

        qualitricsTabHeaderList = []
        
        for qualitricsTabHeader in studentQualitricsTabHeaderList:
            qualitricsTabHeaderList.append(qualitricsTabHeader[0] + '|' + qualitricsTabHeader[1])

        context = {
            'studentUid' : student_uid,
            'studentDetailsDict' : studentDetailsDict,
            'studentFormerNamesList' : StudentFormerNamesList,
            'tabsLists' : qualitricsTabHeaderList,
            # 'tabQualitricsData' : studentQualitricsdata,
            'enrollmentHistoryDetailsList' : studentEnrollmentHistoryList,
            'courseDetailsList' : StudentCourseRequest
            #'commentsList' : commentsList
        }

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return render(request, 'students/studentDetailedView.html', context)


def studentQualitricsYearWiseDetails(request):
    
    try:
        
        if request.method == 'POST':
            studentUid = request.POST['studentUid']
            academicYear = request.POST['academicYear']

            StudentQualitricsDataList = studentsDAL.studentYearWiseQualitricsData(studentUid,academicYear)
            
            #print(StudentQualitricsDataList)

            context = {
                'StudentQualitricsDataList' : StudentQualitricsDataList
            }

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return JsonResponse(context)



def exportcsv(request):

    try:

        if request.method == 'POST':
            username = request.POST['username']
            uid = request.POST['uid']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            campusOfenrollment = request.POST['campusOfenrollment']
            #studentType = request.POST['studentType']
            dcPartner = request.POST['dcPartner']
            currentlyEnrolled = request.POST['currentlyEnrolled']
            #pendingEnrollmentReq = request.POST['pendingEnrollmentReq']

            studentsList = studentsDAL.studentsList(username, uid, firstname, lastname, campusOfenrollment, dcPartner, currentlyEnrolled)
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=students.csv'
            writer = csv.writer(response, delimiter=',')

            response.write(u'\ufeff'.encode('utf8'))

            writer.writerow(['PRSN_UNIV_ID','Student Name', 'DC Partner', 'Course Choice', 'Second Course Choice', 'CREDITS_COMPLETED','PRSN_GDS_CMP_EMAIL_ADDR','INST_CD'])

            for obj in studentsList:
                writer.writerow([ obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7] ])

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return response





    