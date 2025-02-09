from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Job, SeekerProfile, EmployerProfile, Application  # Import Application
from django.contrib.auth.decorators import login_required  # Import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Message
from django.db.models import Q


def is_employer(user):
    return user.is_staff

def is_seeker(user):
    return not user.is_staff

def welcome(request):
    return render(request, 'FreshHire/welcome.html')

@login_required
def shome(request):
    return render(request, 'FreshHire/shome.html')
@login_required
def ehome(request):
    return render(request,'FreshHire/ehome.html')

def signup_seeker(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password, is_staff = False)
            
            return redirect('login')

    return render(request, 'FreshHire/signup_seeker.html')

@login_required
def edit_profile(request):
    user=request.user.seekerprofile
    profile=SeekerProfile.objects.filter(user=request.user)
    if request.method == "POST":
        skills = request.POST.get('skills')
        education = request.POST.get('education')
        resume = request.FILES.get('resume')
        profile_picture = request.FILES.get('profile_picture')  
        if profile_picture:
            user.profile_picture = profile_picture

        user.skills=skills
        user.education=education
        user.resume=resume
       
        user.save()
        
        
        return redirect('my_profile')

    return render(request, 'FreshHire/edit_profile.html',{'profile':profile})

def signup_employer(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password,is_staff = True)
            
            user.save()
           
            return redirect('login')

    return render(request, 'FreshHire/signup_employer.html')


@login_required
def eedit_profile(request):
    user=request.user.employerprofile
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        company_description = request.POST.get('description')
        logo = request.FILES.get('logo')
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
               user.profile_picture=profile_picture
        user.company_name=company_name
        user.company_description=company_description
        user.logo=logo
        user.save()
        

       
        return redirect('emy_profile')

    return render(request, 'FreshHire/eedit_profile.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_seeker(user):
                return redirect('shome')
            elif is_employer(user):
                return redirect('ehome')
        else:
           return redirect('login')
    return render(request, 'FreshHire/login.html')

@login_required
def job_listings(request):
    jobs = Job.objects.all()
    return render(request, 'FreshHire/job_listings.html', {'jobs': jobs})

@login_required
def seeker_profile(request):
    try:
        seeker_profile = SeekerProfile.objects.get(user=request.user)
    except SeekerProfile.DoesNotExist:
        seeker_profile = None
    return render(request, 'FreshHire/seeker_profile.html', {'seeker_profile': seeker_profile})

@login_required
def employer_profile(request):
    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        employer_profile = None
    return render(request, 'FreshHire/employer_profile.html', {'employer_profile': employer_profile})

@login_required
def seeker_dashboard(request):
    try:
        seeker_profile = SeekerProfile.objects.get(user=request.user)
        applied_jobs = Application.objects.filter(seeker=seeker_profile)
    except SeekerProfile.DoesNotExist:
        seeker_profile = None
        applied_jobs = None
    return render(request, 'FreshHire/shome.html', {'seeker_profile': seeker_profile, 'applied_jobs': applied_jobs})

@login_required
def employer_dashboard(request):
    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
        posted_jobs = Job.objects.filter(employer=employer_profile)
    except EmployerProfile.DoesNotExist:
        employer_profile = None
        posted_jobs = None
    return render(request, 'FreshHire/ehome.html', {'employer_profile': employer_profile, 'posted_jobs': posted_jobs})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def my_profile(request):
    user=request.user 
    profile=  SeekerProfile.objects.filter(user=user) 
    return render(request, 'FreshHire/my_profile.html', {'profile': profile},)

@login_required
def emy_profile(request):
    user=request.user 
    profile=  EmployerProfile.objects.filter(user=user) 
    return render(request, 'FreshHire/emy_profile.html', {'profile': profile},)   

@login_required
def post_job(request):

    if request.method== 'POST':
        title= request.POST.get('title')
        description=request.POST.get('description')
        
        job=Job(title=title,description=description,employer=request.user.employerprofile )
        job.save()
        return redirect('mylistings')

    return render(request, 'FreshHire/post_job.html')

@login_required
def job_listings(request):
    jobs= Job.objects.all(); 
    return render(request, 'FreshHire/job_listings.html',{'jobs':jobs}) 

@login_required
def job_details(request,job_id ):
    job=get_object_or_404(Job, id=job_id)

    return render(request, 'FreshHire/job_detail.html',{'job':job})


@login_required
def application(request,job_id):
    job=get_object_or_404(Job, id=job_id)

    if request.method=='POST':
       cover_letter=request.POST.get('cover_letter')
       application=Application(job=job, seeker=request.user.seekerprofile,cover_letter=cover_letter)

       if Application.objects.filter(job=job,seeker=request.user.seekerprofile).exists():
           return redirect('job_listings')
       else:
           application.save()
           return redirect('myapplications')
           
                   
    else:
        return render(request,'FreshHire/job_application.html',{'job':job})
    

@login_required
def my_applications(request):
    user=request.user.seekerprofile
    applications=Application.objects.filter(seeker=user)

    return render(request,'FreshHire/seeker_applications.html',{'applications':applications}) 

@login_required
def my_listings(request):
    employer = request.user.employerprofile  
    jobs = Job.objects.filter(employer=employer)  
    return render(request, 'FreshHire/employer_listings.html', {'jobs': jobs})





@login_required
def employer_job_applications(request):
   
    employer = request.user.employerprofile  
    jobs = Job.objects.filter(employer=employer)  

    applications = []
    # For each job let get the applications
    for job in jobs:
        job_applications = Application.objects.filter(job=job)
        applications.append({
            'job': job,
            'applications': job_applications
        })
    
    return render(request, 'FreshHire/employer_applicants.html', {'applications': applications})    




@login_required
def application_detail(request,application_id):
   
    application = get_object_or_404(Application, id=application_id)

  
    return render(request, 'FreshHire/application_detail.html', {'application': application})


@login_required

def chat(request, seeker_id, employer_id):
    messages = Message.objects.filter(
        (Q(sender_id=seeker_id, recipient_id=employer_id) | 
         Q(sender_id=employer_id, recipient_id=seeker_id))
    ).order_by('timestamp')
    
    if request.method == "POST":
        content = request.POST['content']
        sender = request.user
        recipient = User.objects.get(id=seeker_id if sender.id == employer_id else employer_id)
        Message.objects.create(sender=sender, recipient=recipient, content=content)
    
    return render(request, 'FreshHire/chat.html', {'messages': messages})


@login_required
def chat_list(request):
   
    employer = request.user
    messages = Message.objects.filter(
        Q(sender=employer) | Q(recipient=employer)
    ).order_by('-timestamp')
    
    # Get unique chat partners
    chat_partners = set()
    for message in messages:
        if message.sender != employer:
            chat_partners.add(message.sender)
        if message.recipient != employer:
            chat_partners.add(message.recipient)
    
    return render(request, 'FreshHire/employer_chatlist.html', {'chat_partners': chat_partners})




@login_required
def schat_list(request):
    seeker = request.user
    # Retrieve all messages where the seeker is the sender or recipient
    messages = Message.objects.filter(
        Q(sender=seeker) | Q(recipient=seeker)
    ).order_by('-timestamp')
    
    # Get unique chat partners (employers)
    chat_partners = set()
    for message in messages:
        if message.sender != seeker:
            chat_partners.add(message.sender)
        if message.recipient != seeker:
            chat_partners.add(message.recipient)
    
    return render(request, 'FreshHire/seeker_chatlist.html', {'chat_partners': chat_partners})

@login_required
def schat_detail(request, employer_id, seeker_id):
    messages = Message.objects.filter(
        (Q(sender_id=employer_id, recipient_id=seeker_id) | 
         Q(sender_id=seeker_id, recipient_id=employer_id))
    ).order_by('timestamp')
    
    if request.method == "POST":
        content = request.POST['content']
        sender = request.user
        recipient = User.objects.get(id=employer_id if sender.id == seeker_id else seeker_id)
        Message.objects.create(sender=sender, recipient=recipient, content=content)
    
    return render(request, 'FreshHire/schat_detail.html', {'messages': messages})
