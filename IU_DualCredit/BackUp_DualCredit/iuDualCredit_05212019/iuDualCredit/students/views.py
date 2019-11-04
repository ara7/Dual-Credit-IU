from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Student, ClassData
from django.db import connection
from django.http import JsonResponse
import csv

# Create your views here.
def index(request):
    # courses = Course.objects.all()
    
    #paginator = Paginator(courses, 10)
    #page = request.GET.get('page')
    #paged_listings = paginator.get_page(page)

    #context = {
        #'courses' : paged_listings
        # 'courses' : courses
    #}
    #return render(request, 'courses/search.html',context)

    campusList = [str(classData.CAMPUS) for classData in ClassData.objects.all()]
    campuses = set(campusList)
    
    context = {
      'campuses' : campuses
    }

    return render(request, 'students/search.html', context)


def studentSearch(request):
    
    '''queryset_list = Student.objects.all()
    
    if 'user_name' in request.GET:
        user_name = request.GET['user_name']
        if user_name:
            queryset_list = queryset_list.filter(username__icontains=user_name) 

    if 'uid' in request.GET:
        uid = request.GET['uid']
        if uid:
            queryset_list = queryset_list.filter(uid__iexact=uid) 

    if 'first_name' in request.GET:
        first_name = request.GET['first_name']
        if first_name:
            queryset_list = queryset_list.filter(firstname__iexact=first_name) 

    if 'last_name' in request.GET:
        last_name = request.GET['last_name']
        if last_name:
            queryset_list = queryset_list.filter(lastname__iexact=last_name) 

    if 'campus_of_enrollment' in request.GET:
        campus_of_enrollment = request.GET['campus_of_enrollment']
        if campus_of_enrollment:
            queryset_list = queryset_list.filter(campusofenrollment__iexact=campus_of_enrollment)
    
    if 'student_type' in request.GET:
        student_type = request.GET['student_type']
        if student_type:
            queryset_list = queryset_list.filter(studenttype__iexact=student_type) 

    if 'dc_partner' in request.GET:
        dc_partner = request.GET['dc_partner']
        if dc_partner:
            queryset_list = queryset_list.filter(dcpartner__iexact=dc_partner)     

    #paginator = Paginator(queryset_list, 10)
    #page = request.GET.get('page')
    #paged_listings = paginator.get_page(page)'''


    sqlStudentDetailsQuery = "SELECT student."'"University_ID"'", student."'"First_Name"'", student."'"Last_Name"'", \
        student."'"Academic_Plan_Code"'", student."'"Academic_Program_Code"'", \
        student."'"Institution_Code"'",  \
        student."'"GDS_Campus_Email_Address"'"  \
        from students_student student  \
        where 1=1  "
        #inner join enrollments_Enrollments enrollment \
        #on student."'"University_ID"'" = enrollment."'"PRSN_UNIV_ID"'" "

    username = request.GET.get('username', None)
    uid = request.GET.get('uid', None)
    firstname = request.GET.get('firstname', None)
    lastname = request.GET.get('lastname', None)
    campusOfenrollment = request.GET.get('campusOfenrollment', None)
    studentType = request.GET.get('studentType', None)
    dcPartner = request.GET.get('dcPartner', None)
    currentlyEnrolled = request.GET.get('currentlyEnrolled', None)
    pendingEnrollmentReq = request.GET.get('pendingEnrollmentReq', None)
    
    if username:
        sqlStudentDetailsQuery = sqlStudentDetailsQuery + " AND student."'"Network_ID"'" = '" + username +"'"
            
    if uid:
        sqlStudentDetailsQuery = sqlStudentDetailsQuery + " AND student."'"University_ID"'" = '" + uid + "'"

    if firstname:
        sqlStudentDetailsQuery = sqlStudentDetailsQuery + " AND student."'"First_Name"'" = '" + firstname + "'"

    if lastname:
        sqlStudentDetailsQuery = sqlStudentDetailsQuery + " AND student."'"Last_Name"'" = '" + lastname + "'"

    if campusOfenrollment:
        sqlStudentDetailsQuery = sqlStudentDetailsQuery + " AND classdata."'"Campus_Of_Enrollment"'" = '" + campusOfenrollment + "'"
            
    if studentType:
        sqlStudentDetailsQuery = sqlStudentDetailsQuery + " AND student."'"Student_Type"'" = '" + studentType + "'"

    if dcPartner:
        sqlStudentDetailsQuery = sqlStudentDetailsQuery + " AND student."'"dc_Partner"'" = '" + dcPartner + "'"

    if currentlyEnrolled:
        sqlStudentDetailsQuery = sqlStudentDetailsQuery + " AND student."'"Currently_Enrolled"'" = '" + currentlyEnrolled + "'"
    
    if pendingEnrollmentReq:
        sqlStudentDetailsQuery = sqlStudentDetailsQuery + " AND student."'"Pending_Enrollment_Req"'" = '" + pendingEnrollmentReq + "'"

    print(sqlStudentDetailsQuery)

    cursor = connection.cursor()
    cursor.execute(sqlStudentDetailsQuery)
    rowStudentDetail = cursor.fetchall()

    #print(rowStudentDetail)

    context = {
        #'students' : paged_listings
        'studentDetails': rowStudentDetail,
    }
    #return render(request, 'students/search.html', context)
    return JsonResponse(context)


def studentDetailView(request, student_uid):
    

    # Student Details
    sqlStudentDetailsQuery = "SELECT student."'"First_Name"'", student."'"Last_Name"'", student."'"University_ID"'", \
        student."'"Academic_Plan_Code"'", student."'"Academic_Program_Code"'", \
        student."'"Institution_Code"'",  \
        student."'"GDS_Campus_Email_Address"'"  \
        from students_student student  \
        where student."'"University_ID"'" = '" +  str(student_uid) +"'"

    cursorStudentDetails = connection.cursor()
    cursorStudentDetails.execute(sqlStudentDetailsQuery)
    rowsStudentDetails = cursorStudentDetails.fetchone()
    
    StudentDetailsList = []
    for row in rowsStudentDetails:
        StudentDetailsList.append(row)
    
    #Former Names
    sqlStudentFormerNamesQuery = "SELECT student."'"First_Name"'" \
        from students_student student  \
        where student."'"University_ID"'" = '" +  str(student_uid) +"'"

    cursorStudentFormerNames = connection.cursor()
    cursorStudentFormerNames.execute(sqlStudentFormerNamesQuery)
    rowsStudentFormerNames = cursorStudentFormerNames.fetchall()


    studentFormerNamesList = []
    for row in rowsStudentFormerNames:
        studentFormerNameDict = {}
        rowstudentFormerName = list(row)
        studentFormerNameDict['Student Name'] = rowstudentFormerName[0]
        studentFormerNamesList.append(studentFormerNameDict)

    # Student Details Dictionary
    studentDetailsDict1 = {}
    studentDetailsDict2 = {}
    studentDetailsDict3 = {}
    studentDetailsDict4 = {}

    studentDetailsDict1['Student Name'] = StudentDetailsList[0] + " " + StudentDetailsList[1]
    studentDetailsDict1['User Name'] = 'None'
    studentDetailsDict1['UID'] = StudentDetailsList[2]
    studentDetailsDict1['Date of Birth'] = 'None'
    studentDetailsDict1['Citizenship'] = 'None'
    studentDetailsDict1['Student Type'] = 'None'

    studentDetailsDict2['Legal Sex'] = 'None'
    studentDetailsDict2['Gender Identity'] = 'None'
    studentDetailsDict2['Phone Number'] = 'None'
    studentDetailsDict2['Contact Method'] = 'None'
    studentDetailsDict2['Email'] = 'None'


    studentDetailsDict3['Current Mailing Address'] = 'None'
    studentDetailsDict3['Permanent Mailing Address'] = 'None'
    studentDetailsDict3['Residency'] = 'None'

    studentDetailsDict4['Documents Send under another name'] = 'None'

    #print(rowsStudentFormerNames)

    #Tabs
    sqlTabsQuery = "SELECT enrollment."'"ACAD_TERM_CD"'" \
        from enrollments_enrollments enrollment  \
        where enrollment."'"PRSN_UNIV_ID"'" = '" +  str(student_uid) +"'"

    cursorsqlTabs = connection.cursor()
    cursorsqlTabs.execute(sqlTabsQuery)
    rowTabs = cursorsqlTabs.fetchall()
    
    tabsLists = []
    for row in rowTabs:
        tabsDict = {}
        rowTabsList = list(row)
        tabsDict['Tabs'] = rowTabsList[0]
        tabsLists.append(tabsDict)

    
    print(tabsLists)
    

    # Enrollment History
    '''sqlEnrollmentHistoryQuery = "SELECT enrollment."'"CRS_SUBJ_CD"'", enrollment."'"CLS_NBR"'", enrollment."'"ACAD_TERM_CD"'", \
        enrollment."'"Academic_Plan_Code"'", enrollment."'"Academic_Program_Code"'", enrollment."'"Institution_Code"'",  enrollment."'"GDS_Campus_Email_Address"'" \
        from enrollments_enrollments enrollment  \
        inner join courses_classdata courses \
        on enrollment."'"CRS_ID"'" = courses."'"CRS_ID"'" \
        where enrollment."'"PRSN_UNIV_ID"'" = '" +  str(student_uid) +"'"'''
    
    sqlEnrollmentHistoryDetailsQuery = "SELECT enrollment."'"CRS_SUBJ_CD"'", enrollment."'"CLS_NBR"'", enrollment."'"ACAD_TERM_CD"'" \
        from enrollments_enrollments enrollment  \
        inner join courses_classdata courses \
        on enrollment."'"CRS_ID"'" =  courses."'"CRS_ID"'" \
        where enrollment."'"PRSN_UNIV_ID"'" = '" +  str(student_uid) +"'"
    

    sqlEnrollmentHistoryGPAGraduateWorkQuery = "SELECT enrollment."'"CRS_OFCL_GRD_CD"'", enrollment."'"ACAD_TERM_CD"'" \
        from enrollments_enrollments enrollment  \
        where enrollment."'"PRSN_UNIV_ID"'" = '" +  str(student_uid) +"'"

    cursorEnrollmentHistoryDetails = connection.cursor()
    cursorEnrollmentHistoryDetails.execute(sqlEnrollmentHistoryDetailsQuery)
    rowsEnrollmentHistoryDetails = cursorEnrollmentHistoryDetails.fetchall()

    #print(rowsEnrollmentHistoryDetails)
    #print(sqlEnrollmentHistoryDetailsQuery)

    cursorEnrollmentHistoryGPAGraduateWork = connection.cursor()
    cursorEnrollmentHistoryGPAGraduateWork.execute(sqlEnrollmentHistoryGPAGraduateWorkQuery)
    rowsEnrollmentHistoryGPAGraduateWork = cursorEnrollmentHistoryGPAGraduateWork.fetchone()

    #print(rowsEnrollmentHistoryGPAGraduateWork)

    enrollmentHistoryDetailsList = []
    for row in rowsEnrollmentHistoryDetails:
        enrollmentHistoryDict = {}
        rowEnrollmentHistory = list(row)
        enrollmentHistoryDict['Course'] = rowEnrollmentHistory[0]
        enrollmentHistoryDict['Class'] = rowEnrollmentHistory[1]
        enrollmentHistoryDict['Term'] = rowEnrollmentHistory[2]
        enrollmentHistoryDict['Funding'] = 'None'
        enrollmentHistoryDict['Enrollment'] = 'None'
        enrollmentHistoryDict['Grade'] = 'None'
        enrollmentHistoryDict['Credit Hours'] = 'None'
        enrollmentHistoryDetailsList.append(enrollmentHistoryDict)
        #rowEnrollmentHistoryDetailsList = list(row)
        #enrollmentHistoryDetailsList.append(rowEnrollmentHistoryDetailsList)

    enrollmentHistoryGPAGraduateWork = []
    for row in rowsEnrollmentHistoryGPAGraduateWork:
        enrollmentHistoryGPAGraduateWork.append(row)
    

    enrollmentHistoryGPAGraduateWorkDict = {}
    enrollmentHistoryGPAGraduateWorkDict['GPA'] = enrollmentHistoryGPAGraduateWork[0]
    enrollmentHistoryGPAGraduateWorkDict['Hours of Graduate Work Completed'] = enrollmentHistoryGPAGraduateWork[1]

    #enrollmentHistoryGPAGraduateWorkDict = {}
    #enrollmentHistoryGPAGraduateWorkDict['GPA'] = enrollmentHistoryGPAGraduateWork[0]
    #enrollmentHistoryGPAGraduateWorkDict['Hours of Graduate Work Completed'] = enrollmentHistoryGPAGraduateWork[1]

    # Course Details
    sqlCourseDetails = " SELECT courses."'"CLS_NBR"'", courses."'"CRS_ID"'" \
            From enrollments_Enrollments enrollment \
            inner join  courses_classdata courses \
            on enrollment."'"CRS_ID"'" =  courses."'"CRS_ID"'" \
            Where enrollment."'"PRSN_UNIV_ID"'" = '" + str(student_uid) + "'"
    
    cursorCourseDetails = connection.cursor()
    cursorCourseDetails.execute(sqlCourseDetails)
    rowsCourseDetails = cursorCourseDetails.fetchall()

    courseDetailsList = []
    for row in rowsCourseDetails:
        courseDetailsDict = {}
        rowCourseDetailsList = list(row)
        courseDetailsDict['Requested'] = 'None'
        courseDetailsDict['Choice Number'] = 'None'
        courseDetailsDict['Course Number'] = rowCourseDetailsList[1]
        courseDetailsDict['Class Number'] = rowCourseDetailsList[0]
        courseDetailsDict['Decision Date'] = 'None'
        courseDetailsDict['Decision'] = 'None'
        courseDetailsList.append(courseDetailsDict)
    
    #print(courseDetailsList)

    # Comments
    '''sqlCommnets = " SELECT courses."'"Date"'", courses."'"Comment"'", courses."'"Username"'"   \
            From comments comment \
            Where comment."'"PRSN_UNIV_ID"'" = '" + student_uid + "'"
    
    cursorComments = connection.cursor()
    cursorComments.execute(sqlCommnets)
    rowsComments = cursorComments.fetchall()
    
    commentsList = []
    for row in rowsComments:
        commentsDict = {}
        rowCommentsList = list(row)
        commentsDict['Date'] = rowCommentsList[0]
        commentsDict['Comment'] = rowCommentsList[1]
        commentsDict['Username'] = rowCommentsList[2]
        commentsList.append(courseDetailsDict)'''
    
    context = {
        'studentDetailsDict1' : studentDetailsDict1,
        'studentDetailsDict2' : studentDetailsDict2,
        'studentDetailsDict3' : studentDetailsDict3,
        'studentDetailsDict4' : studentDetailsDict4,
        'studentFormerNamesList' : studentFormerNamesList,
        'tabsLists' : tabsLists,
        'enrollmentHistoryDetailsList' : enrollmentHistoryDetailsList,
        'enrollmentHistoryDict' : enrollmentHistoryGPAGraduateWorkDict,
        'courseDetailsList' : courseDetailsList
        #'commentsList' : commentsList
    }

    return render(request, 'students/studentDetailedView.html', context)


def studentYearWiseDetails(request):
    
    sqlQuery = "SELECT classdata."'"id"'", classdata."'"CRS_ID"'", enrollment."'"CRS_DESC"'", classdata."'"CAMPUS"'", classdata."'"ACAD_TERM_CD"'", \
        classdata."'"CLS_INSTR_NM"'", classdata."'"ENROLLMENT_CAP"'", classdata."'"ENROLLMENT_TOTAL"'",  \
        classdata."'"ENROLLMENT_CAP"'" - classdata."'"ENROLLMENT_TOTAL"'" \
        from courses_classdata classdata \
        inner join enrollments_Enrollments enrollment \
        on classdata."'"CRS_ID"'" = enrollment."'"CRS_ID"'" \
        inner join students_student student \
        on student."'"University_ID"'" = enrollment."'"PRSN_UNIV_ID"'" "
    
    studentUid = request.GET.get('studentUid', None)
    academicYear = request.GET.get('academicYear', None)
    
    if studentUid:
        sqlQuery = sqlQuery + " AND student."'"University_ID"'" = " + studentUid 
            
    if academicYear:
        sqlQuery = sqlQuery + " AND enrollment."'"ACAD_TERM_CD"'" = '" + academicYear + "'"


    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    rows = cursor.fetchall()
    
    queryset_list = []
    for row in rows:
        queryset_list.append(row)
    
    context = {
        'studentYearWiseDetails' : queryset_list,
    }
    
    return JsonResponse(context)


def exportcsv(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        uid = request.POST['uid']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        #campusOfenrollment = request.POST['campusOfenrollment']
        #studentType = request.POST['studentType']
        #dcPartner = request.POST['dcPartner']
        #currentlyEnrolled = request.POST['currentlyEnrolled']
        #pendingEnrollmentReq = request.POST['pendingEnrollmentReq']

        
    queryset_list = Student.objects.all()

    '''if term != 'Select':
        if term:
            #print(termId)
            queryset_list = queryset_list.filter(ACAD_TERM_CD__iexact=term.strip()) 

    if coursenumber != 'Select':
        queryset_list = queryset_list.filter(CRS_ID__iexact=coursenumber.strip())'''
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'
    writer = csv.writer(response, delimiter=',')

    response.write(u'\ufeff'.encode('utf8'))

    writer.writerow(['University_ID','Appl_Nbr','Effective_Date','Academic_Plan_Code','Academic_Program_Code','Institution_Code','First_Name','Last_Name','GDS_Campus_Email_Address' ])

    for obj in queryset_list:
        writer.writerow([ obj.University_ID,obj.Appl_Nbr,obj.Effective_Date,obj.Academic_Plan_Code,obj.Academic_Program_Code,obj.Institution_Code,obj.First_Name,obj.Last_Name,obj.GDS_Campus_Email_Address ])
    
    #print(response)

    return response