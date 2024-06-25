from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Sale
from django.db.models import Sum
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@csrf_protect
def home(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        sale = Sale.objects.create(
            amount=amount
        )

        if sale is not None:
            messages.success(request, 'Sale amount added successfully!')
            return redirect('home')
    return render(request, 'home.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')  # Replace 'home' with your home page URL name
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')









@csrf_protect
@login_required
def admin_view(request):
    sales_list = Sale.objects.all().order_by('-createdAt')

    # Filter sales by date if form is submitted
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        sales_list = sales_list.filter(createdAt__date__gte=start_date, createdAt__date__lte=end_date)

    # Pagination
    paginator = Paginator(sales_list, 10)  # Show 10 sales per page
    page = request.GET.get('page')

    try:
        sales = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sales = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sales = paginator.page(paginator.num_pages)

    sales_count = sales_list.count()
    total_sales_amount = sales_list.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        "sales": sales,
        "sales_count": sales_count,
        "total_sales_amount": total_sales_amount,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, 'admin.html', context)
