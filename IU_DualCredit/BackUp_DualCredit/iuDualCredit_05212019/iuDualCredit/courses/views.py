from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import ClassData, Enrollments
from django.utils.encoding import smart_str
from django.db import connection
from django.http import JsonResponse
import csv

# Create your views here.
def index(request):
    # courses = Course.objects.all()
    
    termList = [str(classData.ACAD_TERM_CD) for classData in ClassData.objects.all()]
    campusList = [str(classData.CAMPUS) for classData in ClassData.objects.all()]

    terms = set(termList)
    campuses = set(campusList)
    
    context = {
      'terms' : terms,
      'campuses' : campuses
    }
    return render(request, 'courses/search.html', context)

def courseSearch(request):
    #queryset_list = ClassData.objects.all()
    
    #cursor = connection.cursor()
    #cursor.execute("SELECT a."'"CRS_ID"'",  a."'"ACAD_TERM_CD"'" from courses_classdata a inner join enrollments_Enrollments b  on a."'"CRS_ID"'" = b."'"CRS_ID"'"")
    #rows = cursor.fetchall()
    
    #queryset_list = []
    # print(rows)

    # very important
    '''for row in rows:
        print(row)
        for i in range(0, len(row)):
            print(row[i])'''

    '''cursor.execute(" SELECT classdata."'"CRS_ID"'", enrollment."'"CRS_DESC"'", classdata."'"ACAD_TERM_CD"'", classdata."'"CAMPUS"'", .\
        classdata."'"CLS_INSTR_NM"'", classdata."'"ENROLLMENT_CAP"'", classdata."'"ENROLLMENT_TOTAL"'",   .\
        classdata."'"ENROLLMENT_CAP"'" - classdata."'"ENROLLMENT_TOTAL"'" ""Calculated Remaning"" .\
        from courses_classdata classdata .\
        inner join enrollments_Enrollments enrollment .\
        on classdata."'"CRS_ID"'" = enrollment."'"CRS_ID"'" ")'''

    '''for obj in queryset_list:
        #print(obj.CRS_ID)
        #courseID = obj.CRS_ID
        #print(courseID[0])
        #obj.enrollment.add()

        enroll = Enrollments.objects.all().filter(CRS_ID = obj.CRS_ID)
        obj.enrollment = enroll
        #print(enrollment)
        #print(obj.CRS_ID + " " + obj.enrollment.CRS_DESC)
    
        # x = Enrollments.objects.filter(CRS_ID = 93494)
        # for a in x:
        # print(a.CLS_NBR)

        i = 0
        classdata = ClassData
        classdata.CLS_NBR = row[i]
        i  = i+1
        classdata.CRS_ID = row[i]
        i  = i+1
        classdata.ACAD_TERM_CD = row[i]
        i  = i+1
        classdata.CLS_INSTR_NM = row[i]
        i  = i+1
        classdata.CAMPUS = row[i]
        i  = i+1
        classdata.ENROLLMENT_CAP = row[i] 
        i  = i+1
        classdata.ENROLLMENT_TOTAL = row[i]'''

    #print("hello")
    #print(coursenumber)


    sqlQuery = "SELECT classdata."'"id"'", classdata."'"CRS_ID"'", enrollment."'"CRS_DESC"'", classdata."'"CAMPUS"'", classdata."'"ACAD_TERM_CD"'", \
        classdata."'"CLS_INSTR_NM"'", classdata."'"ENROLLMENT_CAP"'", classdata."'"ENROLLMENT_TOTAL"'",  \
        classdata."'"ENROLLMENT_CAP"'" - classdata."'"ENROLLMENT_TOTAL"'" \
        from courses_classdata classdata \
        inner join enrollments_Enrollments enrollment \
        on classdata."'"CRS_ID"'" = enrollment."'"CRS_ID"'" "
    
    coursenumber = request.GET.get('coursenumber', None)
    coursename = request.GET.get('coursename', None)
    campusinstructions = request.GET.get('campusinstructions', None)
    term = request.GET.get('term', None)

    if coursenumber:
        sqlQuery = sqlQuery + " AND classdata."'"CRS_ID"'" = " + coursenumber 
            
    if coursename:
        sqlQuery = sqlQuery + " AND enrollment."'"CRS_DESC"'" = '" + coursename + "'"

    if campusinstructions:
        sqlQuery = sqlQuery + " AND classdata."'"CAMPUS"'" = '" + campusinstructions + "'"

    if term:
        sqlQuery = sqlQuery + " AND classdata."'"ACAD_TERM_CD"'" = " + term
    
    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    rows = cursor.fetchall()
    
    queryset_list = []
    for row in rows:
        queryset_list.append(row)
    
    termList = [str(classData.ACAD_TERM_CD) for classData in ClassData.objects.all()]
    campusList = [str(classData.CAMPUS) for classData in ClassData.objects.all()]

    terms = set(termList)
    campuses = set(campusList)

    context = {
        'terms' : list(terms),
        'campuses' : list(campuses),
        'courses' : queryset_list,
        'values': request.GET
    }

    return JsonResponse(context)


def courseDetailView(request, course_id):
    #course = get_object_or_404(Course, pk=course_id)
    #courseDetail = ClassData.objects.all().filter(CRS_ID__iexact=str(course_id))
    #print(courseDetail.ClassData.CLS_NBR + " " + courseDetail.ClassData.CRS_ID)
    #for x in courseDetail:
    #print(x.CLS_NBR)
    
    #print("Hello")
    #print(course_id)

    #termList = [str(classData.ACAD_TERM_CD) for classData in ClassData.objects.all()]
    #terms = set(termList)
    
    sqlCourseDetails = "SELECT enrollment."'"CRS_DESC"'", classdata."'"ACAD_TERM_CD"'", classdata."'"CAMPUS"'", \
            classdata."'"ENROLLMENT_CAP"'" - classdata."'"ENROLLMENT_TOTAL"'", \
            classdata."'"ENROLLMENT_CAP"'", classdata."'"ENROLLMENT_TOTAL"'"  \
            from courses_classdata classdata \
            inner join enrollments_Enrollments enrollment \
            on classdata."'"CRS_ID"'" = enrollment."'"CRS_ID"'" "
    
    sqlCourseDetails = sqlCourseDetails + " AND classdata."'"CRS_ID"'" = " + str(course_id)

    cursorCourseDetails = connection.cursor()
    cursorCourseDetails.execute(sqlCourseDetails)
    rowsCourseDetails = cursorCourseDetails.fetchone()

    queryCourseDetailsList = []
    courseee = ClassData() 
    for row in rowsCourseDetails:
        queryCourseDetailsList.append(row)

    #Dictionary

    #Course Details
    courseDetailsDict = {}
    courseDetailsDict['Course Description'] = queryCourseDetailsList[0]
    courseDetailsDict['Term Offered'] = queryCourseDetailsList[1]
    courseDetailsDict['Campus of Instruction'] = queryCourseDetailsList[2]
    courseDetailsDict['Number of Drops'] = 'None'
    courseDetailsDict['Number of Withdrawals'] = 'None'

    #course Sections
    courseSectionDict = {}

    #seats
    seatsDict = {}
    seatsDict['Total Seats'] = queryCourseDetailsList[5]
    seatsDict['Enrolled'] = queryCourseDetailsList[4]
    seatsDict['Calculated Remaining'] = queryCourseDetailsList[3]
    seatsDict['Pending Enrollment'] = 'None'

    #print(courseDetailsDict)
    

    sqlStudentDetails = " SELECT studentdata."'"First_Name"'", studentdata."'"Middle_Name"'", studentdata."'"Last_Name"'"   \
            From students_student studentdata \
            WHERE studentdata."'"University_ID"'" IN \
            (SELECT enrollment."'"PRSN_UNIV_ID"'" \
            From enrollments_Enrollments enrollment \
            Where enrollment."'"CRS_ID"'" = " + str(course_id) + ") "

    #cursorStudentDetails = connection.cursor()
    #cursorStudentDetails.execute(sqlStudentDetails)
    #rowsStudentDetails = cursorStudentDetails.fetchall()
    
    cursorStudentDetails = connection.cursor()
    cursorStudentDetails.execute(sqlCourseDetails)
    rowsStudentDetails = cursorStudentDetails.fetchall()
    
    studentDetailsList = []
    #print(rowsStudentDetails)
    for row in rowsStudentDetails:
        studentDetailsDict = {}
        rowstudentDetailsList = list(row)
        studentDetailsDict['Student Name'] = rowstudentDetailsList[0]
        studentDetailsDict['Section'] = rowstudentDetailsList[1]
        studentDetailsDict['Course Status'] = rowstudentDetailsList[2]
        studentDetailsList.append(studentDetailsDict)
        #print(rowstudentDetailsList)
        #rowstudentDetailsList = row.split(",")
        #studentDetailsList.append(rowstudentDetailsList)

    print(studentDetailsList)
    
    context = {
        'CourseDetails' : queryCourseDetailsList,
        'courseDetailsDict' : courseDetailsDict,
        'seatsDict' : seatsDict,
        'StudentDetails' : studentDetailsList,
        'courseId' : course_id
    }
    
    return render(request, 'courses/courseDetailedView.html', context)
    #return JsonResponse(context)
    #return HttpResponse(request, 'courses/courseDetailedView.html', context)


def exportcsv(request):
    
    if request.method == 'POST':
        coursenumber = request.POST['coursenumber']
        coursename = request.POST['coursename']
        #campusinstructions = request.POST['campusinstructions']
        #term = request.POST['term']

    queryset_list = ClassData.objects.all()

    '''if term != 'Select':
        if term:
            #print(termId)
            queryset_list = queryset_list.filter(ACAD_TERM_CD__iexact=term.strip()) 

    if coursenumber != 'Select':
        queryset_list = queryset_list.filter(CRS_ID__iexact=coursenumber.strip())'''
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=courses.csv'
    writer = csv.writer(response, delimiter=',')

    response.write(u'\ufeff'.encode('utf8'))

    writer.writerow(['CLS_NBR', 'CRS_ID' , 'ACAD_TERM_CD', 'CLS_INSTR_NM', 'CLS_INSTR_GDS_CMP_EMAIL_ADDR', 'CAMPUS', 'ENROLLMENT_CAP', 'ENROLLMENT_TOTAL' ])

    for obj in queryset_list:
        writer.writerow([ obj.CLS_NBR, obj.CRS_ID, obj.ACAD_TERM_CD, obj.CLS_INSTR_NM, obj.CLS_INSTR_GDS_CMP_EMAIL_ADDR, obj.CAMPUS, obj.ENROLLMENT_CAP, obj.ENROLLMENT_TOTAL ])
    
    #print(response)

    return response