from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import user
from django.utils import timezone
import random, requests, os

sms_signature = os.getenv('sms_signature')

def register(req):
    if req.method == 'GET':
        return render(req, 'register.html', {'submit':'ارسال کد تایید'})
    else:
        #info level
        if req.POST['submit'] == 'ارسال کد تایید':
            data = {'submit': req.POST['submit'], 'email':req.POST['email'], 'phone':req.POST['phone'], 'name':req.POST['name'], 'password':req.POST['password'], 'cnf_password':req.POST.get('cnf_password')}
            #check password and confirm
            if req.POST.get('password') != req.POST.get('cnf_password'):
                data['error'] = 'کلمه عبور با تکرار آن مطابق نیست!'
                return render(req, 'register.html', data)
            #check email
            if '@' not in req.POST.get('email') or '.' not in req.POST.get('email'):
                data['error'] = 'ایمیل وارد شده معتبر نیست'
                return render(req, 'register.html', data)
            User = user.objects.filter(phone=data.get('phone'))
            #check phone if it's not available
            if User and User[0].verified_phone: 
                data['error'] = 'این شماره قبلا ثبت شده است'
                return render(req, 'register.html', data)
            #check if phone is in database but it's not verified
            elif User and not User[0].verified_phone:
                User = User[0]
                User.name = data['name'].encode()
                User.email = data['email']
                User.set_password(data['password'])
                User.save()
            #create a new user
            elif not User:
                User = user.objects.create_user(data.get('email'), data.get('phone'), data.get('name').encode(), data.get('password'))
            #send code
            User.verification_code = random.randint(10000, 99999)
            User.verification_code_time = timezone.now()
            User.save()
            params = {'sender': '10004346', 'receptor': User.phone, 'message': f'کد تایید در applier: \n {User.verification_code}'} 
            text = f'کد تایید شما در گالری آموزش: \n {User.verification_code}'
            p = requests.get(f'http://sms.parsgreen.ir/UrlService/sendSMS.ashx?from=10001398&to={User.phone}&&text={text}&signature={sms_signature}')
            if 'Invalid' in p.content.decode():
                data.update({'error':'شماره تلفن صحیح نمی باشد'})
                return render(req, 'register.html', data)
            else:
                data.update({'submit':'تایید'})
                return render(req, 'register.html', data)
             
        #verify level
        else:
            data = {'submit': req.POST['submit'], 'email':req.POST['email'], 'phone':req.POST['phone'], 'name':req.POST['name'], 'password':req.POST['password'], 'cnf_password':req.POST['cnf_password']}
            User = user.objects.filter(phone=data.get('phone'))
            #check if user changed the  phone
            if not User:
                data['error'] = 'شماره تلفن صحیح نمی باشد'
                return render(req, 'register.html', data)  
            #check verification code
            if str(User[0].verification_code) != req.POST.get('verification_code') or (timezone.now()-User[0].verification_code_time).total_seconds()>120:
                data['error'] = 'کد تایید معتبر نمی باشد'
                return render(req, 'register.html', data) 
            User[0].verified_phone = True
            User[0].save()
            auth.login(req, User[0])
            return redirect('home')


def login(req):
    if req.method == 'GET':
        return render(req, 'login.html')
    User = user.objects.filter(phone=req.POST['phone'])
    if User and User[0].check_password(req.POST['password']) and User[0].verified_phone:
        auth.login(req, User[0])
        return redirect('home')
    return render(req, 'login.html', {'error':'کاربری با این اطلاعات یافت نشد'})

@login_required(login_url='login')
def dashboard(req):
    return render(req, 'panel-dashboard.html')

@login_required(login_url='login')
def edit_password(req):
    User = req.user
    if req.method == 'GET':
        return render(req, 'panel-edit-password.html')
    if not User.check_password(req.POST['password']):
        return render(req, 'panel-edit-password.html', {'error':'رمز عبور اشتباه است'})
    if req.POST['new_password'] != req.POST['cnf_new_password']:
        return render(req, 'panel-edit-password.html', {'error':'رمز عبور جدید با تکرار آن همخوانی ندارد'})
    User.set_password(req.POST['new_password'])
    User.save()
    return render(req, 'panel-edit-password.html', {'alert':'رمز شما با موفقیت عوض شد'})
    
@login_required(login_url='login')
def my_courses(req):
    return render(req, 'panel-my-courses.html')

def logout(req):
    auth.logout(req)
    return redirect('home')