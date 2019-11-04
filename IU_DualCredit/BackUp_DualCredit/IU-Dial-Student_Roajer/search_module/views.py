from django.shortcuts import render
from django.views import View
from .models import *
from django.db.models import Q


class SearchScreenView(View):
    """Landing page / Search screen View"""

    def get(self, request):
        students = Student.objects.all()
        return render(request, 'search_screen.html', {'students': students, })

# ------------------------ Student Module -----------------------------------


class StudentSearchView(View):
    """Student Search View"""

    def post(self, request):
        print(request.POST)
        students = Student.objects.filter(Q(username__icontains=request.POST['username']) | Q(uid__icontains=request.POST['uid']) | Q(
            first_name__icontains=request.POST['first_name']) | Q(last_name__icontains=request.POST['last_name']) | Q(campus_of_enrollment__icontains=request.POST['enrollment_campus']) | Q(student_type__icontains=request.POST['student_type']) | Q(dc_partner__icontains=request.POST['dc_partner']))
        print("Search Results : ", students)
        return render(request, 'search_screen.html', {'students': students, })


class StudentDetailsView(View):
    """Student Details View"""

    def get(self, request, student_id):
        student = Student.objects.get(uuid=student_id)
        return render(request, 'student_details.html', {'student': student, })


class UpdateStudentUidView(View):
    """Student Uid Update View"""

    def post(self, request, student_id):
        student = Student.objects.get(uuid=student_id)
        student.uid = request.POST['uid']
        student.save()
        return render(request, 'student_details.html', {'student': student, })


class AddCommentView(View):
    """Add Comment"""

    def post(self, request):
        print(request.POST)
        pass


# ------------------------ Course Module -----------------------------------


class CourseDetailsView(View):
    """Course Details View"""

    def get(self, request):
        return render(request, 'course_details.html')

# ----------------------- Enrollment Module ---------------------------------


class EnrollmentDetailsView(View):
    """Enrollment Details View"""

    def get(self, request):
        return render(request, 'enrollment_details.html')
