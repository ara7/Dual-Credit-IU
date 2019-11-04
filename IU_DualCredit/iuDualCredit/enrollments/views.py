from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Enrollments
from django.utils.encoding import smart_str
from django.db import connection
from django.http import JsonResponse
import csv
from DAL import enrollmentsDAL 
from helpers import logging
import sys
from datetime import datetime

def index(request):

    try:

        
        termList = enrollmentsDAL.termList()
        courseList = enrollmentsDAL.courseList()
        fundingList = enrollmentsDAL.fundingList()

        context = {
        'terms' : termList,
        'courses' : courseList,
        'fundings' : fundingList
        }

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return render(request, 'enrollments/search.html', context)    
    


def search(request):

    try:

        term = request.GET.get('term', None)
        if term:
            termCd = enrollmentsDAL.GetAcadTermCode(term)
        else:
            termCd = None
        
        course = request.GET.get('course', None)
        funding = request.GET.get('funding', None)
        
        if funding:
            fundingId = enrollmentsDAL.GetFundingId(funding)
        else:
            fundingId = None

        termList = enrollmentsDAL.termList()
        courseList = enrollmentsDAL.courseList()
        enrollmentDetailsList = enrollmentsDAL.enrollmentList(termCd,course,fundingId)

        context = {
            'terms' : termList,
            'courses' : courseList,
            'enrollments' : enrollmentDetailsList,
            'values': request.GET
        }

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return JsonResponse(context)    
    


def exportcsv(request):
    

    try:

        if request.method == 'POST':
            term = request.POST['term']
            course = request.POST['course']
            funding = request.POST['funding']

            if term:
                termCd = enrollmentsDAL.GetAcadTermCode(term)
            else:
                termCd = None

            if funding:
                fundingId = enrollmentsDAL.GetFundingId(funding)
            else:
                fundingId = None

            enrollmentDetailsExportList = enrollmentsDAL.enrollmentList(termCd,course,fundingId)

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=enrollment.csv'
            writer = csv.writer(response, delimiter=',')

            response.write(u'\ufeff'.encode('utf8'))

            writer.writerow(['ACAD_TERM_CD', 'CRS_SUBJ_CD' , 'Funding', 'STUDENT_ENRL_ADD_DT', 'UserName' ])

            for obj in enrollmentDetailsExportList:
                writer.writerow([ obj[0], obj[1], obj[5], obj[2], obj[3] ])
    
    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)
    
    finally:
        return response    


    