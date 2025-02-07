from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('signup_seeker/', views.signup_seeker, name='signup_seeker'),
    path('signup_employer/', views.signup_employer, name='signup_employer'),
    path('login/', views.login_user, name='login'),
    path('job_listings/', views.job_listings, name='job_listings'),
    path('seeker_profile/', views.seeker_profile, name='seeker_profile'),
    path('employer_profile/', views.employer_profile, name='employer_profile'),
    path('seeker_dashboard/', views.seeker_dashboard, name='seeker_dashboard'),
    path('employer_dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('seeker_profile_creation/', views.edit_profile, name='edit_profile'),
    path('employer_profile_creation/', views.eedit_profile, name='eedit_profile'),
    path('seekerdashboard/', views.seeker_dashboard, name='seeker_dashboard'),
    path('myprofile/', views.my_profile, name='my_profile' ),
    path('emyprofile/', views.emy_profile, name='emy_profile'),
    path('postjob/', views.post_job, name='post_job'),
    path('joblistings/', views.job_listings, name='job_listings'),
    path('jobdetails/<int:job_id>', views.job_details, name='job_details'),
    path('application/<int:job_id>', views.application, name='application'),
    path('myapplications/' , views.my_applications, name='myapplications'),
    path('mylistings/', views.my_listings, name='mylistings'),
    path('your-job-applications/', views.employer_job_applications, name='employer_job_applications'),
    path('applicationdetail/<int:application_id>', views.application_detail, name='application_detail'),
    path('chat/<int:seeker_id>/<int:employer_id>/', views.chat, name='chat'),
    path('chat-list/', views.chat_list, name='chat_list'),
    path('schat-list/', views.schat_list, name='schat_list'),
    path('chat/<int:sender_id>/<int:receiver_id>/', views.schat_detail, name='chat_detail'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)