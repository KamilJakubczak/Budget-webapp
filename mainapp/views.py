from django.shortcuts import render,get_object_or_404,redirect
from datetime import datetime, date
# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Entry, SubCategory, Category, Payment
from .forms import EntryForm
from django.db.models import Sum
import json
from django.core.serializers.json import DjangoJSONEncoder

import read_csv
mapping = {
    #Transfer 
    'cash_inc': 1,
    'account_exp': 2,
    'cshToAcc': 3,
    'account_inc': 4,
    'cash_exp': 5,
    'accToRet': 6,
    'retToAcc': 7,
    'accToTar': 8,
    'tarToAcc': 9,
    'accToEmr': 10,
    'emrToAcc': 11,
    'accToEnt': 12,
    'entToAcc': 13,
    'accToCsh': 14,
    'retToTB' : 15,
    'TBToRet' : 16,
    

    'income': 2,
    'expenditures': 1,
   
    }

def load_types(request):
    types_id = request.GET.get('type')
    categories = Category.objects.filter(parent_type_name_id=types_id)
    return render(request, 'mainapp/type_dropdown_list_options.html', {'categories': categories})

def load_categories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(parent_category_name_id=category_id)#category_id)#.order_by('citi_name')
    return render(request, 'mainapp/category_dropdown_list_options.html', {'subcategories': subcategories})

def load_payments(request):
    print('vies.payments')
    types_id = request.GET.get('payment')
    payments = Payment.objects.filter(parent_type_name_id=types_id)
    return render(request, 'mainapp/payment_dropdown_list_options.html', {'payments': payments})

#def month_view()
def view_month(request,year,month):
    if month !=12:
        next_month = f'{year}-{month+1}-01'
    else:
        next_month = f'{year+1}-01-01'

    yearly_sum = Entry.objects.filter(transaction_date__year__lte=year)
    to_month_sum = Entry.objects.filter(transaction_date__lte=next_month)

    monthly_sum = yearly_sum.filter(transaction_date__month=month)
    temp_month = month
    years = Entry.objects.values_list('transaction_date__year').distinct()
    categs = get_categories_list(monthly_sum)
    tempyear=[]
    tempmonths=[]
    for year in years:
        tempyear.append(year[0])
    year = None
    years = tempyear
    months = Entry.objects.values_list('transaction_date__month').distinct()
    
    for month in months:
        tempmonths.append(month[0])
    month = temp_month
    months=tempmonths
   
    details = monthly_sum.order_by('-transaction_date')

    account_sum = payment_result(to_month_sum,'account_inc','account_exp','amount')
    account_sum += payment_result(to_month_sum,'retToAcc','accToRet','amount')
    account_sum += payment_result(to_month_sum,'emrToAcc','accToEmr','amount')
    account_sum += payment_result(to_month_sum,'tarToAcc','accToTar','amount')
    account_sum += payment_result(to_month_sum,'entToAcc','accToEnt','amount')
    account_sum += payment_result(to_month_sum,'cshToAcc','accToCsh','amount')
    account_sum = round(float(account_sum),2)

    treasury_bonds_ret_sum = payment_result(to_month_sum,'retToTB','TBToRet','amount')
    retirement_sum = payment_result(to_month_sum,'accToRet','retToAcc','amount')
    retirement_sum += payment_result(to_month_sum,'TBToRet','retToTB','amount')
    emergency_sum = payment_result(to_month_sum,'accToEmr','emrToAcc','amount')
    target_sum = payment_result(to_month_sum,'accToTar','tarToAcc','amount')    
    entertainment_sum = payment_result(to_month_sum,'accToEnt','entToAcc','amount')
    savings_sum = retirement_sum+emergency_sum+target_sum+entertainment_sum

    
    cash_sum = payment_result(to_month_sum,'cash_inc','cash_exp','amount')
    cash_sum += payment_result(to_month_sum,'accToCsh','cshToAcc','amount')

    income_sum = getTypeSum(monthly_sum,mapping['income'])
    expenditures_sum = getTypeSum(monthly_sum,mapping['expenditures'])
    result_sum = round(income_sum - expenditures_sum,2)
    income_sum =income_sum
    chart_percentage =[]
    chart_values =[]
    chart_labels =[]
    chart_values.append(income_sum)
    chart_values.append(expenditures_sum)
    chart_labels.append('result')
    chart_labels.append('expenditures')
    income_prc = (income_sum-expenditures_sum)/income_sum
    if(income_prc < 0):
        income_prc = 0
    exp_prc = expenditures_sum/(income_sum)
    if(exp_prc > 1):
        exp_prc = 1
    chart_percentage.append(income_prc)
    chart_percentage.append(exp_prc)
    categories_amount = get_categories_amount(details,categs)
    json_values = json.dumps(chart_values, cls=DjangoJSONEncoder)
    json_percentage = json.dumps(chart_percentage,cls=DjangoJSONEncoder)
    json_labels = json.dumps(chart_labels)
    json_categories = json.dumps(categs)
    json_categories_amount = json.dumps(categories_amount,cls=DjangoJSONEncoder)
    contex = {'account_sum': account_sum,
            'cash_sum': cash_sum,
            'income_sum': income_sum,
            'expenditures_sum': expenditures_sum,
            'details': details,
            'month': month,
            'result_sum': result_sum,
            'retirement_sum': retirement_sum,
            'emergency_sum': emergency_sum,
            'target_sum': target_sum,
            'entertainment_sum': entertainment_sum,
            'savings_sum': savings_sum,
            'treasury_bonds_ret': treasury_bonds_ret_sum,
            'years': years,
            'months': months,
            'json_labels': chart_labels,
            'json_values': chart_values,
            'json_categories': json_categories,
            'json_categories_amount': json_categories_amount,
            'json_percentage':json_percentage,
            }
    return render(request, 'mainapp/view_all.html',contex)

def get_categories_list(monthly_sum):
    category_list = monthly_sum.filter(types =mapping['expenditures']).values_list('category')
    
    temp_list = []
    for i in category_list:
        temp_list.append(i[0])
    category_list = set(category_list)
    ready_list =[]
    for cat in category_list:
        ready_list.append(((Category.objects.filter(id=cat[0]).values_list('category_name'))[0])[0])
    print('function list' + str(ready_list))
    return ready_list

def get_categories_amount(monthly_sum, category_list):
    amount_list =[]
    for category in category_list:
        temp_amount = monthly_sum.filter(category__category_name=category).aggregate(Sum('amount'))
        amount_list.append(temp_amount['amount__sum'])

    return amount_list


def full_list(request):

    years = Entry.objects.values_list('transaction_date__year').distinct()
    
    tempyear=[]
    tempmonths=[]
    for year in years:
        tempyear.append(year[0])
    year = None
    years = tempyear
    months = Entry.objects.values_list('transaction_date__month').distinct()
    
    for month in months:
        tempmonths.append(month[0])
    months=tempmonths

    current_month = datetime.now().month
    get_all = Entry.objects.all()
    details = get_all.order_by('-transaction_date')
    monthly_sum = Entry.objects.all()

    account_sum = payment_result(monthly_sum,'account_inc','account_exp','amount')
    account_sum += payment_result(monthly_sum,'retToAcc','accToRet','amount')
    account_sum += payment_result(monthly_sum,'emrToAcc','accToEmr','amount')
    account_sum += payment_result(monthly_sum,'tarToAcc','accToTar','amount')
    account_sum += payment_result(monthly_sum,'entToAcc','accToEnt','amount')
    account_sum = round(float(account_sum),2)
    retirement_sum = payment_result(monthly_sum,'accToRet','retToAcc','amount')
    emergency_sum = payment_result(monthly_sum,'accToEmr','emrToAcc','amount')
    target_sum = payment_result(monthly_sum,'accToTar','tarToAcc','amount')    
    entertainment_sum = payment_result(monthly_sum,'accToEnt','entToAcc','amount')
    savings_sum = retirement_sum+emergency_sum+target_sum+entertainment_sum

    cash_sum = payment_result(monthly_sum,'cash_inc','cash_exp','amount')
    income_sum = getTypeSum(monthly_sum,mapping['income'])
    expenditures_sum = getTypeSum(monthly_sum,mapping['expenditures'])
    if income_sum == None:
        income_sum =0
    if expenditures_sum == None:
        expenditures_sum = 0
    result_sum = income_sum - expenditures_sum

    contex = {'account_sum': account_sum,
            'cash_sum': cash_sum,
            'income_sum': income_sum,
            'expenditures_sum': expenditures_sum,
            'details': details,
            'current_month': current_month,
            'result_sum': result_sum,
            'retirement_sum': retirement_sum,
            'emergency_sum': emergency_sum,
            'target_sum': target_sum,
            'entertainment_sum': entertainment_sum,
            'savings_sum': savings_sum,
            'years': years,
            'months': months,}
    return render(request, 'mainapp/view_all.html',contex)
def add2(request):
    today = date.today().strftime('%Y-%m-%d')
    return render(request,'mainapp/entry_form2.html',{'today': today})

def new_entry(request):
    form = EntryForm(request.POST)
    form.save()
    return HttpResponseRedirect(reverse('transactions'))

def getTypeSum(dataset,transaction_type):
    output = dataset.filter(types=transaction_type).aggregate(Sum('amount'))['amount__sum']
    if output == None:
        output =0
    return float(output)


def payment_result(data,pos_amount,neg_amount,col):
    try:
        pos_sum = data.filter(payment=mapping[pos_amount]).aggregate(Sum(col))
        pos_sum = pos_sum[col+'__sum']
    except:
        pos_sum = 0
    try:
        neg_sum = data.filter(payment=mapping[neg_amount]).aggregate(Sum(col))
        neg_sum = neg_sum[col+'__sum']
    except:
        neg_sum = 0
    if pos_sum == None:
        pos_sum =0
    if neg_sum == None:
        neg_sum =0
    result = float(pos_sum) - float(neg_sum)
    return round(result,2)

def savings_graph(request):
    years = Entry.objects.values_list('transaction_date__year').order_by('transaction_date__year').distinct()
    year_month = []
    amounts = []
    ret_sum = []
    emr_sum = []
    tar_sum = []
    ent_sum = []
    ret = 0
    emr = 0
    tar = 0
    ent = 0

    for year in years:
        months = Entry.objects.values_list('transaction_date__month').order_by('transaction_date__month').distinct()
        for month in months:
            year_month.append(str(year[0]) + '-' + str(month[0]))
            year_month_data = Entry.objects.filter(transaction_date__year=year[0]).filter(transaction_date__month=month[0])
            ret += payment_result(year_month_data,'accToRet','retToAcc','amount')
            emr += payment_result(year_month_data,'accToEmr','emrToAcc','amount')
            tar += payment_result(year_month_data,'accToTar','tarToAcc','amount')
            ent += payment_result(year_month_data,'accToEnt','entToAcc','amount')                                 
            ret_sum.append(ret)
            emr_sum.append(emr)
            tar_sum.append(tar)
            ent_sum.append(ent)



    json_dates = json.dumps(year_month)
    json_ret = json.dumps(ret_sum, cls=DjangoJSONEncoder)
    json_emr =json.dumps(emr_sum,cls=DjangoJSONEncoder)    
    json_tar =json.dumps(tar_sum,cls=DjangoJSONEncoder)
    json_ent =json.dumps(ent_sum,cls=DjangoJSONEncoder)    
    content ={
        'json_dates': json_dates,
        'json_ret': json_ret,
        'json_emr': json_emr,
        'json_tar': json_tar,
        'json_ent': json_ent
    }
    return render(request,'mainapp/test.html',content)

def del_entry(request,entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(Entry,pk=entry_id)
        entry.delete()
        return redirect('view_all')

def show_transactions(request):
    transactions = read_csv.TransactionList('/home/noxiss/Downloads/lista_operacji_200201_200229_202003071553459319.csv')
    transactions_list = transactions.transactions
    return render(request,'mainapp/transaction_view.html',{'transactions': transactions_list})