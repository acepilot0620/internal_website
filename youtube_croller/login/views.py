from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from .models import Account

# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST['id']
        password = request.POST["password"]
        
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, "회원정보가 일치하지 않습니다.")
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')

def signup(request):
    if request.method == "POST":
        user_id = request.POST.get('id')
        position = request.POST.get('position')
        nickname = request.POST.get('nickname')
        user_password1 = request.POST.get('password1')
        user_password2 = request.POST.get('password2')



        if user_id == ""or nickname =="" or position == "" or user_password1 == "" or user_password2 == "":
            messages.info(request,"모든 항목을 채워주세요.")
            return redirect('signup')
        
                # 비밀번호가 다를 때
        if not user_password1 == user_password2:
            messages.info(request, "비밀번호가 다릅니다.")
            return redirect('signup')

        
        user = User.objects.create_user(username=user_id, password=user_password1)
        user.save()
        account = Account(user=user, position=position, nickname=nickname)
        account.save()
        return redirect('login')
    else:
        return render(request, 'signup.html')

