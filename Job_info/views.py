from datetime import date

import mysql.connector
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

from Job_info.models import Applicant, Company, Job, Applications, AdminPanel


# User
def user_signup(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        state = request.POST.get('state')
        location = request.POST.get('location')

        if password != confirm_password:
            return HttpResponse('password do not match')

        if len(password) < 8:
            return HttpResponse('please enter minimum 8 digit password')

        try:
            Applicant.objects.get(email=email)
            return HttpResponse("you are already a user please login")
        except Applicant.DoesNotExist:
            pass

        user1 = Applicant(fullname=fullname, dob=dob, email=email, password=password,
                          confirm_password=confirm_password, mobile=mobile, gender=gender, state=state,
                          location=location)

        user1.save()
        return HttpResponse('completed')

        # try:
        #     user = Applicant.objects.get(email=email)
        #     if user.email == email:
        #         return HttpResponse("you are already a user please login")
        # except Applicant.DoesNotExist:
        #     user1 = Applicant(first_name=first_name, last_name=last_name, dob=dob, email=email, password=password,
        #                       confirm_password=confirm_password, mobile=mobile, gender=gender, state=state,
        #                       location=location)
        #     user1.save()
        #     return HttpResponse('completed')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            AdminPanel.objects.get(email=email)
        except AdminPanel.DoesNotExist:
            return HttpResponse('please enter a valid email-id')

        try:
            AdminPanel.objects.get(password=password)
        except AdminPanel.DoesNotExist:
            return HttpResponse('please enter a valid password')

    return HttpResponse('welcome')

    # user = Applicant.objects.get(Q(email=email) & Q(password=password))


def search(request):
    location = request.GET.get('location')
    title = request.GET.get('title')
    company = request.GET.get('company')

    dbconnect = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin123',
        database='the_right_path')

    crs = dbconnect.cursor()
    if location:
        query = "select * from the_right_path.job_info_job where location='" + location + "' "
        crs.execute(query)

    elif title:
        query = "select * from the_right_path.job_info_job where title='" + title + "' "
        crs.execute(query)
    elif company:
        query = "select * from the_right_path.job_info_job company='" + company + "' "
        crs.execute(query)

    data = crs.fetchall()

    # return HttpResponse(data)
    results = []
    for row in data:
        result = {
            'id': row[0],
            'title': row[1],
            'location': row[2],
            'company': row[3],
            'description': row[4],
            'skills_req': row[5],
            'date_posted': row[6]

        }
        results.append(result)

    return JsonResponse({'results': results})


def apply(request):
    if request.method == 'POST':
        # company = request.POST.get('company')
        job_id = request.POST.get('job_id')
        applicant_id = request.POST.get('applicant_id')
        email = request.POST.get('email')
        experience = request.POST.get('experience')
        photo = request.POST.get('photo')
        resume = request.POST.get('resume')

        try:
            Applicant.objects.get(email=email)
        except Applicant.DoesNotExist:
            return HttpResponse('please signup first')

        applicant = Applicant.objects.get(id=applicant_id)
        job = Job.objects.get(id=job_id)

        date1 = date.today()
        if job.end_date < date1:
            return HttpResponse('this job is no longer available')

        elif job.start_date > date1:
            return HttpResponse('job not open yet')

        else:
            application = Applications(applicant=applicant, job=job, company=job.company_id, experience=experience,
                                       photo=photo, resume=resume, apply_date=date.today())

            application.save()
    return HttpResponse('completed')


# Company


def company_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(password) < 8:
            return HttpResponse("please enter minimum 8 digit password")

        if password != confirm_password:
            return HttpResponse('password do not match')

        try:
            Company.objects.get(email=email)
            return HttpResponse("you are already a user please login")
        except Company.DoesNotExist:
            pass

        user1 = Company(username=username, email=email, password=password,
                        confirm_password=confirm_password, company_name=company_name)
        user1.save()
        return HttpResponse('completed')


# def create_job(request):
#     if request.method == 'POST':
#         company = request.POST.get('company_id')
#         title = request.POST.get('title')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         location = request.POST.get('location')
#         salary = request.POST.get('salary')
#         description = request.POST.get('description')
#         experience = request.POST.get('experience')
#         skills = request.POST.get('skills')
#
#         # obj = Company.objects.filter(id=company).values()
#         # print(type(obj[0].get('id')))
#         # print(type(int(company)))
#
#     try:
#         obj = Company.objects.filter(id=company).values()
#         if obj[0].get('id') == int(company):
#             obj1 = Job(company=company, title=title, location=location, description=description, skills=skills,
#                        salary=salary, experience=experience, start_date=start_date, end_date=end_date)
#             obj1.save()
#             return HttpResponse('completed')
#     except Company.DoesNotExist:
#         return HttpResponse("Please Enter A Valid Company-Id ")

def create_job(request):
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        description = request.POST.get('description')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')

        try:
            obj = company = Company.objects.get(id=company_id)
            print(obj.id)
        except Company.DoesNotExist:
            return HttpResponse("Please Enter A Valid Company-Id ")

        obj1 = Job(company=company, title=title, location=location, description=description, skills=skills,
                   salary=salary, experience=experience, start_date=start_date, end_date=end_date)
        obj1.save()
        return HttpResponse('completed')


#
# def edit_job(request):
#     if request.method == "POST":
#         title = request.POST.get('title')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         salary = request.POST.get('salary')
#         experience = request.POST.get('experience')
#         location = request.POST.get('location')
#         skills = request.POST.get('skills')
#         description = request.POST.get('description')
#         company_id = request.POST.get('company_id')
#         myid = request.POST.get('id')
#
#         # try:
#         #     Job.objects.get(company_id=company_id)
#         # except Job.DoesNotExist:
#         #     return HttpResponse('please login first')
#         # job = Job.objects.get(id=myid)
#         try:
#             job = Job.objects.get(id=myid)
#         except Job.DoesNotExist:
#             return HttpResponseBadRequest("Invalid Job id")
#
#         job.title = title
#         job.salary = salary
#         job.experience = experience
#         job.location = location
#         job.skills = skills
#         job.description = description
#
#         job.save()
#
#         if start_date:
#             job.start_date = start_date
#             job.save()
#         if end_date:
#             job.end_date = end_date
#             job.save()
#     return HttpResponse('completed')

def update_job(request):
    id = request.GET['id']
    try:
        job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        return HttpResponseBadRequest("Invalid Job id")

    # Update job fields if provided in request
    if 'title' in request.GET:
        job.title = request.GET['title']
    if 'experience' in request.GET:
        job.experience = request.GET['experience']
    if 'description' in request.GET:
        job.description = request.GET['description']
    if 'location' in request.GET:
        job.location = request.GET['location']
    if 'skill' in request.GET:
        job.skills = request.GET['skill']
    if 'salary' in request.GET:
        job.salary = request.GET['salary']
    if 'start_date' in request.GET:
        job.start_date = request.GET['start_date']
    if 'end_date' in request.GET:
        job.end_date = request.GET['end_date']

    job.save()
    return HttpResponse('Job updated successfully')


# Admin Panel

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

    admin = AdminPanel(username=username, email=email, password=password)
    admin.save()
    return HttpResponse('completed')


def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            AdminPanel.objects.get(username=username)
        except AdminPanel.DoesNotExist:
            return HttpResponse('please enter a valid email-id')

        try:
            AdminPanel.objects.get(password=password)
        except AdminPanel.DoesNotExist:
            return HttpResponse('please enter a valid password')

    return HttpResponse('welcome')


def view_applicants(request):
    if request.method == 'POST':
        username = request.POST['username']

        try:
            AdminPanel.objects.get(username=username)
        except AdminPanel.DoesNotExist:
            return HttpResponse('not a valid person')
    applicants = Applicant.objects.all()

    applicant_data = []
    for applicant in applicants:
        data = {
            'id': applicant.id,
            'fullname': applicant.fullname,
            'email': applicant.email,
            'dob': applicant.dob,
            'gender': applicant.gender,
            'mobile': applicant.mobile,
            'state': applicant.state,
            'location': applicant.location,
            'password': applicant.password
        }
        applicant_data.append(data)

    return JsonResponse({'applicants': applicant_data})


def pending_jobs(request):
    jobs = Job.objects.filter(is_approved=False).values()
    return JsonResponse({'jobs': list(jobs)})


def change_status(request):
    id = request.GET['id']
    status = request.GET['status']
    try:
        jobs = Job.objects.get(id=id)
    except Job.DoesNotExist:
        return HttpResponse('please enter a valid id')

    jobs.is_approved = status
    jobs.save()

    return HttpResponse('completed')


def accepted_jobs(request):
    jobs = Job.objects.filter(is_approved=True).values()
    return JsonResponse({'jobs': list(jobs)})


def all_companies(request):
    companies = Company.objects.all()

    companies_data = []
    for company in companies:
        data = {
            'name': company.id,
            'username': company.username,
            'company_name': company.company_name,
            'email': company.email,
            'password': company.password,

        }
        companies_data.append(data)

    return JsonResponse({'companies': companies_data})


def delete_company(request, myid):
    company = Company.objects.filter(id=myid)
    company.delete()
    return HttpResponse('successfully deleted')
