from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import ClassData, Enrollments
from django.utils.encoding import smart_str
from django.db import connection
from django.http import JsonResponse
import csv
import sys
import time
from DAL import coursesDAL 
from DAL import enrollmentsDAL 
from helpers import logging
import sys
from datetime import datetime

# Create your views here.
def index(request):
    
    try:
        termList = coursesDAL.termList()
        campusList = coursesDAL.campusOfInstructionList()
        
        context = {
            'terms' : termList,
            'campuses' : campusList
        }
    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return render(request, 'courses/search.html', context)

def courseSearch(request):
    
    try:

        termList = coursesDAL.termList()
        campusList = coursesDAL.campusOfInstructionList()

        coursenumber = request.GET.get('coursenumber', None)
        coursename = request.GET.get('coursename', None)
        campusinstructions = request.GET.get('campusinstructions', None)

        term = request.GET.get('term', None)
        if term:
            termCd = enrollmentsDAL.GetAcadTermCode(term)
        else:
            termCd = None

        coursesList = coursesDAL.coursesList(coursenumber,coursename,campusinstructions,termCd)
        
        context = {
            'terms' : termList,
            'campuses' : campusList,
            'courses' : coursesList,
            'values': request.GET
        }

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return JsonResponse(context)  


def courseDetailView(request, courseinfo):

    try:

        courseInformation = courseinfo.split("|")
        courseID = courseInformation[0]
        term = courseInformation[1]
        CampusOfInstruction = courseInformation[2]

        if term:
            termCd = enrollmentsDAL.GetAcadTermCode(term)
        else:
            termCd = None

        courseDetailsHeader1List, courseDetailsHeader2List, campusSeatsList, StudentDetailsList  = coursesDAL.courseDetailView(courseID,termCd,CampusOfInstruction)

        # print(courseDetailsHeader1List)
        # print(courseDetailsHeader2List)
        # print(campusSeatsList)
        # print(StudentDetailsList)

        courseDetailsDict = {}
        
        #Course Details
        if courseDetailsHeader1List:
            courseDetailsDict['Course Description'] = courseDetailsHeader1List[1]
            courseDetailsDict['Term Offered'] = courseDetailsHeader1List[2]
            courseDetailsDict['Campus of Instruction'] = courseDetailsHeader1List[4]
        else:
            courseDetailsDict['Course Description'] = 'None'
            courseDetailsDict['Term Offered'] = 'None'
            courseDetailsDict['Campus of Instruction'] = 'None'


        if courseDetailsHeader2List:
            courseDetailsDict['Number of Drops'] = courseDetailsHeader2List[3]
            courseDetailsDict['Number of Withdrawals'] = courseDetailsHeader2List[4]
        else:
            courseDetailsDict['Number of Drops'] = 'None'
            courseDetailsDict['Number of Withdrawals'] = 'None'

        context = {
            'courseDetailsDict' : courseDetailsDict,
            'campusSeatsList' : campusSeatsList,
            'StudentDetailsList' : StudentDetailsList,
            'courseId' : courseID
        }

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return render(request, 'courses/courseDetailedView.html', context)


    

def exportcsv(request):
    
    try:

        if request.method == 'POST':
            coursenumber = request.POST['coursenumber']
            coursename = request.POST['coursename']
            campusinstructions = request.POST['campusinstructions']
            term = request.POST['term']

            if term:
                termCd = enrollmentsDAL.GetAcadTermCode(term)
            else:
                termCd = None

            coursesList = coursesDAL.coursesList(coursenumber,coursename,campusinstructions,termCd)

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename= courses.csv'
            writer = csv.writer(response, delimiter=',')
            response.write(u'\ufeff'.encode('utf8'))

            writer.writerow(['CRS_ID', 'CRS_DESC' , 'ACAD_TERM_CD', 'COI_INST_CD', 'CLS_INSTR_NM', 'ENROLLMENT_CAP', 'ENROLLMENT_TOTAL', 'Calculated_Remaining' ])

            for obj in coursesList:
                writer.writerow([ obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7], obj[8] ])
            
            #print(response)
    
    except:

        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return response


   

    