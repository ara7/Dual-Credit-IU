from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Enrollments
from django.utils.encoding import smart_str
from django.db import connection
from django.http import JsonResponse
import csv

# Create your views here.

def index(request):
    #queryset_dropDown = Enrollments.objects.all()
    #enrollment_term = queryset_dropDown.ACADEMIC_TERM_CD
    #enrollment_Course = queryset_dropDown.crs_subj_cd + " : " + queryset_dropDown.crs_catlg_nbr
    
    termList = [enroll.ACAD_TERM_CD for enroll in Enrollments.objects.all()]
    courseList = [str(enroll.CRS_SUBJ_CD) + " : " + str(enroll.CRS_CATLG_NBR) for enroll in Enrollments.objects.all()]
    
    terms = set(termList)
    courses = set(courseList)
    
    context = {
      'terms' : terms,
      'courses' : courses
    }
    return render(request, 'enrollments/search.html', context)
    

def search(request):
    queryset_list = Enrollments.objects.all()

    termList = [str(enroll.ACAD_TERM_CD) for enroll in queryset_list]
    courseList = [str(enroll.CRS_SUBJ_CD) + " : " + str(enroll.CRS_CATLG_NBR) for enroll in queryset_list]

    terms = set(termList)
    courses = set(courseList)
    
    '''if 'term' in request.GET:
        term = request.GET['term']
        if term:
            queryset_list = queryset_list.filter(ACAD_TERM_CD__iexact=term) 

    if 'course' in request.GET:
        course = request.GET['course']
        crsSubjCd = (course.split(':')[0]).strip()
        CrsCatlgNbr = (course.split(':')[1]).strip()
        if course:
            queryset_list = queryset_list.filter(CRS_SUBJ_CD__iexact=crsSubjCd).filter(CRS_CATLG_NBR__iexact=CrsCatlgNbr) 

    if 'funding' in request.GET:
        funding = request.GET['funding']
        if funding:
            queryset_list = queryset_list.filter(funding__iexact=funding)

    
    #print(queryset_list.query)

    paginator = Paginator(queryset_list, 10)
    # page = request.GET.get('page')
    # paged_listings = paginator.get_page(page) 
    
    page = int(request.GET.get('page', '1'))
    enrollmentDetails = paginator.page(page)
    
    # Get the index of the current page
    # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    # You want a range of 7, so lets calculate where to slice the list
    # Get our new page range. In the latest versions of Django page_range returns
    # an iterator. Thus pass it to list, to make our slice possible again.
    
    index = enrollmentDetails.number - 1  
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]
    
    #print(request.GET)'''

    term = request.GET.get('term', None)
    course = request.GET.get('course', None)
    funding = request.GET.get('funding', None)

    if course:
        crsSubjCd = (course.split(':')[0]).strip()
        CrsCatlgNbr = (course.split(':')[1]).strip()
    
    sqlEnrollmentQuery = "SELECT enrollment."'"ACAD_TERM_CD"'", enrollment."'"CRS_SUBJ_CD"'", \
        enrollment."'"STU_ENRL_ADD_DT"'", enrollment."'"CLS_INSTR_NM"'" \
        from  enrollments_Enrollments enrollment "
    
    if term:
        sqlEnrollmentQuery = sqlEnrollmentQuery + " AND enrollment."'"ACAD_TERM_CD"'" = " + term 
            
    if course:
        sqlEnrollmentQuery = sqlEnrollmentQuery + " AND enrollment."'"CRS_SUBJ_CD"'" = '" + crsSubjCd + "' AND enrollment."'"CRS_CATLG_NBR"'" = '" + CrsCatlgNbr + "'"

    cursor = connection.cursor()
    cursor.execute(sqlEnrollmentQuery)
    enrollmentDetailsList = cursor.fetchall()

    #print(enrollmentDetailsList)

    context = {
        'terms' : list(terms),
        'courses' : list(courses),
        'enrollments' : enrollmentDetailsList,
        #'page_range': page_range,
        'values': request.GET
    }

    #return render(request, 'enrollments/search.html', context)
    return JsonResponse(context)


def exportcsv(request):
    
    if request.method == 'POST':
        termId = request.POST['termID']
        course = request.POST['course']
        funding = request.POST['funding']

    queryset_list = Enrollments.objects.all()

    if termId != 'Select':
        if termId:
            print(termId)
            queryset_list = queryset_list.filter(ACAD_TERM_CD__iexact=termId.strip()) 

    if course != 'Select':
        crsSubjCd = (course.split(':')[0]).strip()
        CrsCatlgNbr = (course.split(':')[1]).strip()
        queryset_list = queryset_list.filter(CRS_SUBJ_CD__iexact=crsSubjCd.strip()).filter(CRS_CATLG_NBR__iexact=CrsCatlgNbr.strip()) 

    if funding != 'Select':
        queryset_list = queryset_list.filter(funding__iexact=funding)

    print(queryset_list)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=enrollment.csv'
    writer = csv.writer(response, delimiter=',')

    response.write(u'\ufeff'.encode('utf8'))

    writer.writerow(['ACAD_TERM_CD', 'CRS_SUBJ_CD' , 'CRS_CATLG_NBR', 'STUDENT_ENRL_ADD_DT', 'CLASS_INSTR_NM' ])

    for obj in queryset_list:
        writer.writerow([ obj.ACAD_TERM_CD, obj.CRS_SUBJ_CD, obj.CRS_CATLG_NBR, obj.STU_ENRL_ADD_DT, obj.CLS_INSTR_NM ])
    
    return response