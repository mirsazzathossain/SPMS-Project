from os import name
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='home'),
    path('stdcwplo', views.studentcoursewiseplo, name='stdcwplo'),
    path('stdpwplo', views.studentprogrmwiseplo, name='stdpwplo'),
    path('stdcourses/', views.getstudentcourses, name='stdcourses'),
    path('plotable', views.PLOacheivementtable, name='plotable'),
    path('facwplo', views.facultycousewisePLO, name='facwplo'),
    path('semcwplo', views.semestercousewisePLO, name='semcwplo'),
    path('plowcour', views.plowisecourseanalysis, name='plowcour'),
    path('semwprogplo', views.semesterwiseploacheivementcntcomp, name='semwprogplo'),
    path('prowplocour', views.programwiseploalnalysisofcourses, name='prowplocour'),
]
