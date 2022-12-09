from django.urls import path
from . import views
from .import helpers


urlpatterns = [
    path('', views.home, name='home'),
    path('report_name_check', views.report_name_check, name='report_name_check'),
    path('query_runner', helpers.query_runner, name='query_runner'),
    path('show_profile', views.show_profile, name='show_profile'),
    path('run_individual_report/<int:pk_>', views.run_individual_report, name='run_individual_report'),
]