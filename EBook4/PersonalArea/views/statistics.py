from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import *

def index(request):
    return render(request, "statistics/index.html")

def year(request, year):
    statistic = SystemReports.objects.get(date__year=int(year))
    return render(request, "statistics/year.html")

def total_statistics(request):
    return render(request, "statistics/total.html")

