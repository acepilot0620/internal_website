#크롤링을 위한 import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
from youtube_croller import parse, instagram_parse


from django.shortcuts import render,redirect, HttpResponse, get_object_or_404
from .models import Youtube_result,Search,Instagram_result,Contract,Record
from login.models import Account

# Create your views here.

def main(request):
    context = {}
    if request.user.is_authenticated:
        contract = Contract.objects.all()
        account = Account.objects.get(user=request.user)
        context.setdefault('contract', contract)
        context.setdefault('nickname', account.nickname)
        context.setdefault('position', account.position)
    if request.method == 'POST':

        youtube_search = request.POST.get('search_youtube')
        condition = request.POST.get('condition')
        insta_search = request.POST.get('search_insta')

        if youtube_search != None:
            condition = int(condition)
            result_list = parse.croller(youtube_search)
            i = 1
            for node in result_list:
                result = Youtube_result()
                result.id = i
                result.channel_name = node.channel_name
                result.subscriber_num = node.subscriber_num
                result.not_int_subscriber_num = node.not_int_subscriber_num
                result.profile_url = node.profile_url
                result.save()
                i +=1
            result_all = Youtube_result.objects.all()
            return render(request,'youtube_result.html',{'search':youtube_search, 'result':result_all, 'condition':condition})
        if insta_search != None:
            result_list,relevent_keyword_list = instagram_parse.insta_croller(insta_search)
            output = ''
            for keyword in relevent_keyword_list:
                output = output + ('#'+keyword + ', ')
                if keyword == relevent_keyword_list[-1]:
                    output = output[:-2]

            i = 1
            for node in result_list:
                result = Instagram_result()
                result.id = i
                result.insta_id = node.insta_id
                result.profile_url = node.profile_url
                result.save()
                i +=1
            result_all = Instagram_result.objects.all()
            return render(request,'instagram_result.html',{'search':insta_search, 'result':result_all, 'relevent_keyword': output})        
    return render(request,'main.html',context)



def go_back_and_clean(request):
    old_youtube_result = Youtube_result.objects.all()
    old_instagram_result = Instagram_result.objects.all()
    old_instagram_result.delete()
    old_youtube_result.delete()
    return redirect('home')

def create_contract(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        category = request.POST.get('category')
        end_date = request.POST.get('end_date')
        new_contract = Contract()
        new_contract.name = company_name
        new_contract.category = category
        new_contract.end_date = end_date
        new_contract.save()
        return redirect('home')
    return render(request,'create_contract.html')

def delete_contract(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    contract.delete()
    return redirect('home')

def show_record(request,contract_id):
    context = {}
    account = Account.objects.get(user=request.user)
    contract = get_object_or_404(Contract,pk=contract_id)
    record = Record.objects.all().filter(contract=contract)
    context.setdefault('account', account)
    context.setdefault('record', record)
    context.setdefault('contract', contract)
    if request.method == 'POST':
        insta_id = request.POST.get('insta_id')
        influencer = request.POST.get('influencer')
        feed_condition = request.POST.get('feed_condition')
        new_record = Record()
        new_record.contract = contract
        new_record.influencer = influencer
        new_record.writer = account.nickname
        new_record.feed_condition = feed_condition
        new_record.is_confirmed = False
        new_record.save()
        return render(request,'contract_board.html',context)
    return render(request,'contract_board.html',context)

def confirm(request, record_id, contract_id):
    contract = get_object_or_404(Contract, pk = contract_id)
    record = Record.objects.get(id=record_id)
    record.is_confirmed = True
    record.save()
    return redirect('/contract_board/'+str(contract_id))

def wait(request, record_id,contract_id):
    contract = get_object_or_404(Contract, pk = contract_id)
    record = Record.objects.get(id=record_id)
    record.is_confirmed = False
    record.save()
    return redirect('/contract_board/'+str(contract_id))

def delete(request, record_id, contract_id):
    contract = get_object_or_404(Contract, pk = contract_id)
    record = Record.objects.filter(contract=contract, id=record_id)
    record.delete()
    return redirect('/contract_board/'+str(contract_id))

 














