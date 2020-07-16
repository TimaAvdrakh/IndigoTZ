import json
import os
from main.employee.models import Employee
os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)


from main.employee.models import Employee

with open("data.json", 'r') as openfile:
    file = json.load(openfile)

for i in file:
    rank = i['rank']
    employee = i['employer']
    count = i['employeesCount']
    median = i['medianSalary']
    employee = Employee(rank=rank, employee=employee,count=count, median=median)
    employee.save()



