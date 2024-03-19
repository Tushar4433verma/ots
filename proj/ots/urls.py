
from django.urls import path
from ots.views import*
from django.contrib.auth import views as auth_views
app_name='ots'
urlpatterns = [
    path('',welcome,name='welcome'),
    path('new-candidate',CandidateRegistrationForm,name='registrationForm'),
    path('store-candidate',CandidateRegistration,name='storeCandidate'),
    path('login',loginView,name='login'),
    path('home',CandidateHome,name="home"),
    path('test-paper',testPaper,name="testpaper"),
    path('calculate-result',CalculateTestResult,name="calculate_test"),
    path('test-history',testResultHistory,name="testHistory"),
    path('result',showTestResult,name="result"),
    path('logout',logoutView,name='logout'),
]
