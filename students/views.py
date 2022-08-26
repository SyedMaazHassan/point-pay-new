from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from dashboard.supporting_func import *
from dashboard.models import *
from dashboard.supporting_func import getUser
from django.contrib import messages
from authentication.decorators import djangoAdminNotAllowed
from payment.models import FeeSubmission

@djangoAdminNotAllowed
@login_required
def students(request, student_id=None):
    user = getUser(request.user)
    all_students = UserInfo.objects.filter(organization = user.organization, status = "student").order_by("-added_at")
    single_student = None
    is_current_paid = False
    if student_id:
        student = all_students.filter(id = student_id).first()
        if not student:
            messages.error(request, "No student exists with the given id")
            return redirect("students:all")
        single_student = student
        is_current_paid_check = FeeSubmission.objects.filter(user = single_student, voucher__month = timezone.now().month)
        is_current_paid = is_current_paid_check.exists()

    context = {
        'page': 'students', 
        'all_students': all_students, 
        'single_student': single_student,
        'is_current_paid': is_current_paid,
        'total_departments': Department.objects.filter(organization = user.organization).count()
    }
    return render(request, "home/students/index.html", context)