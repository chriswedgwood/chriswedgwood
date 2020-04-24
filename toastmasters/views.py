from django.shortcuts import render
import altair as alt
from django.http import JsonResponse
from django.shortcuts import render
from .models import Member

# Create your views here.


def member_summary(request):
    query = Member.objects.all().values()
    data = alt.Data(values=list(query))
    chart_obj = alt.Chart(data).mark_bar().encode(

    )
    return JsonResponse(chart_obj,safe=False)


def index_page(request):
    return render(request,"index_page.html")
