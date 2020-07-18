from django.shortcuts import render
from .models import Employee
from django.http import HttpResponse,FileResponse
from django.core.serializers import serialize
from django.shortcuts import redirect
from .forms import EmployeeFrom
from django.core import serializers
import logging
# logger = logging.getLogger(__name__)
import json
from django.http import JsonResponse

import pickle
import redis
r = redis.Redis(host='localhost', port=6379)
# r.set('employee:deleted', None)
# r.set('employee:added', None)
logging.basicConfig(level=logging.DEBUG, filename='actions.log',format='%(asctime)s %(levelname)s:%(message)s')



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
            logging.info("Adding data to model")
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
        logging.info("Sorted Data by Rank")
    elif to_sort == 'Employer':
        employees = Employee.objects.all().order_by('name')
        logging.info("Sorted Data by Rank")
    elif to_sort == 'Count':
        employees = Employee.objects.all().order_by('-count')
        logging.info("Sorted Data by Rank")
    else:
        employees = Employee.objects.all().order_by('-median')
        logging.info("Sorted Data by Rank")


    return render(request,'list.html',context={'employees': employees,'keys': keys})


def delete_view(request, rank):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    employee = Employee.objects.filter(rank=rank)
    data = pickle.dumps(employee)
    # data = serializers.serialize('json', employee)
    key = 'employee:deleted'
    r.append(key, data)
    ans = r.get('employee:deleted')
    print(pickle.loads(ans))
    employee.delete()
    logging.info("Deleted employee")

    return redirect('list')

def add_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('main:login')
    form = EmployeeFrom(request.POST)
    key = 'employee:added'

    if form.is_valid():
        data = [form.data['rank'], form.data['name']]
        r.append(key, pickle.dumps(data))
        print(r.get(key))
        form.save()
        return redirect('list')


    context['form'] = form
    return render(request, "add.html", context)


def download_data(request):
    queryset = Employee.objects.all()
    data = serializers.serialize('json', queryset)
    with open("sample.json", "w") as outfile:
        outfile.write(data)

    with open("sample.json", 'r') as myfile:
        data = myfile.read()
    response = FileResponse(data)
    response['Content-Type'] = 'application/json'
    return response