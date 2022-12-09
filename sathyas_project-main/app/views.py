from django.shortcuts import render, HttpResponse
import json
from .models import Table, Report
from django.contrib.auth.decorators import login_required
from . helpers import *


# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        query = request.POST.get('query_select')

        if query == 'burt':
            pk = burt_helper(request)
            result, output = query_runner(pk)
            context = {
                'report_obj': Report.objects.get(pk=pk),
                'result': result,
                'output': output
            }
            return render(request, 'burt_result.html', context)
        elif query == 'Jira':
            pass
        elif query == 'QTest':
            pk = burt_helper(request)
            result, output = query_runner_qtest(pk)
            context = {
                'report_obj': Report.objects.get(pk=pk),
                'result': result,
                'output': output
            }
            return render(request, 'burt_result.html', context)
        elif query == 'mixed':
            pk = burt_helper(request) #function call for mixed
            result, output = mixed_query_runner(pk)

            context = {
                'report_obj': Report.objects.get(pk=pk),
                'result': result,
                'output': output
            }

            return render(request, 'burt_result.html', context)
        else:
            pass #function call for jira
    else:
        name = request.user.first_name
        name = name + ' ' + request.user.last_name

        r = Report.objects.get(pk=6)

        context = {
            'name': name,
            'report': r
        }
        return render(request, 'home.html', context)


def report_name_check(request):
    report_name = request.POST.get('report_name')

    if Report.objects.filter(name=report_name).count() > 0:
        return HttpResponse(json.dumps({'status': "1"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': "0"}), content_type="application/json")


@login_required(login_url='login')
def show_profile(request):
    user = request.user
    context = {
        'reports': Report.objects.filter(created_by=user)
    }

    return render(request, 'user_profile.html', context)


@login_required(login_url='login')
def run_individual_report(request, pk_):

    r = Report.objects.get(pk=pk_)
    result, output = [], []

    if r.type_of_report == 'burt':
        result, output = query_runner(pk_)
    elif r.type_of_report == 'QTest':
        result, output = query_runner_qtest(pk_)
    elif r.type_of_report == 'mixed':
        pass
    else:
        pass

    context = {
                'report_obj': r,
                'result': result,
                'output': output
            }
    return render(request, 'burt_result.html', context)