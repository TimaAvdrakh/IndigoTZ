from django.shortcuts import render
from .models import Employee
from django.http import HttpResponse
from django.core.serializers import serialize
from django.shortcuts import redirect
from .forms import EmployeeFrom
from django.core import serializers
import logging
logger = logging.getLogger(__name__)
import json
from django.http import JsonResponse


import redis
r = redis.Redis()
# r.set('employee:deleted', None)
# r.set('employee:added', None)



def load_data(request):
    Employee.objects.all().delete()
    with open('/home/tima/Desktop/indigoTZ/main/data.json') as openfile:
        files = json.load(openfile)
    try:
        for file in files:
            rank = file['rank']
            employee = file['employer']
            count = file['employeesCount']
            median = file['medianSalary']
            employee = Employee(rank=rank, name=employee, count=count, median=median)
            logger.info("Adding data to model")
            employee.save()
    except:
        return HttpResponse("Rank is already in use")

    return redirect('list')


def list_data(request):
    keys = ['Rank', 'Employer',"Count", "MedianSalary"]
    employees = Employee.objects.all().order_by('rank')

    return render(request,'list.html',context={'employees': employees,'keys': keys})

def sorted_data(request,to_sort):

    keys = ['Rank', 'Employer',"Count", "MedianSalary"]
    if to_sort == 'Rank':
        employees = Employee.objects.all().order_by('rank')
        logger.info("Sorted Data by Rank")
    elif to_sort == 'Employer':
        employees = Employee.objects.all().order_by('name')
        logger.info("Sorted Data by Rank")
    elif to_sort == 'Count':
        employees = Employee.objects.all().order_by('-count')
        logger.info("Sorted Data by Rank")
    else:
        employees = Employee.objects.all().order_by('-median')
        logger.info("Sorted Data by Rank")


    return render(request,'list.html',context={'employees': employees,'keys': keys})


def delete_view(request, rank):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    employee = Employee.objects.get(rank=rank)
    key = 'employee:deleted'
    r.rpush=({key:[employee.rank, employee.name]})
    employee.delete()

    print(r.get(key))

    return redirect('list')


def add_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('main:login')
    form = EmployeeFrom(request.POST)
    key = 'employee:added'

    if form.is_valid():
        print(form.data['rank'])
        r.rpush = ({key: [form.data['rank'], form.data['name']]})

        form.save()
        return redirect('list')

    context['form'] = form
    return render(request, "add.html", context)


def download_data(request):
    queryset = Employee.objects.all()
    data = serializers.serialize('json', queryset)
    with open("sample.json", "w") as outfile:
        outfile.write(data)
    return HttpResponse(json.dumps(data), content_type="application/json",)