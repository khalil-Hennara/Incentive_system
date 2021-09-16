from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.forms import inlineformset_factory
from django.utils import timezone
# Create your views here.
from .models import *
from .forms import CreatUserForm,CreatEmployForm,UpdateProfile,Edit_Rate,Priz_form,RateForm,FormRateForm
from .decorator import unauthanticate_user,allowed_users
from  .utils import *

@login_required(login_url='login')
def index(request):
    return render(request,'index.html')

@unauthanticate_user
def login_page(request):
    if request.method=='POST':
       username= request.POST.get('username')
       password=request.POST.get('password')
       user=authenticate(request,username=username,password=password)
       if user is not None:
            login(request,user)
            return redirect('index')
            
       else:
        messages.info(request,'username or password is incorrect')
        #return redirect('login')
    return render(request,'login.html')


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def register_page(request):
    default_img="default.jpg"
    userform=CreatUserForm(prefix='User')
    employeeform=CreatEmployForm(prefix='Employee')
    if request.method=='POST':
        userform=CreatUserForm(request.POST,prefix='User')
        employeeform=CreatEmployForm(request.POST,prefix='Employee')
        if employeeform.is_valid() and userform.is_valid():
            user=userform.save()
            group=Group.objects.get(name='employee')
            user.groups.add(group)
            employee=employeeform.save(commit=False)
            employee.user=user
            boss_id=request.POST['Employee-boss_id']
            boss_obj=Employee.objects.get(id=boss_id)
            level=boss_obj.level+1
            employee.level=level
            employee.save()
            employee.boss_id.add(boss_obj)
            employee.img=default_img
            employee.save()
            return redirect('index')
        
    context={'userform':userform,'employeeform':employeeform}
    return render(request,'register.html',context)



@login_required(login_url='login')
def profile_page(request):
    random_color=['success','danger','info','warning']
    employee=request.user.employee
    rating_list=list(employee.user_rate_set.all())
    rating_list=calculate_rating(rating_list)
    prisList=list(employee.user_price_set.all())
    if len(rating_list):
        prise_point,prise_list=get_point_need(rating_list[-1],prisList)
    else:
        prise_point,prise_list=get_point_need(0,prisList)
    notifications=[]
    is_active=False
    
    if len(prise_list) != 0:
        notification_name="win Prize"
        notification_message="you have win a new prize !!!"
        notifications.append(notification_message)
        notification=User_Notification(employee_id=employee,name=notification_name,message=notification_message)
        notification.save()
        for pr in prise_list:
            obj=user_Price(Price_id=pr,employee_id=employee)
            obj.save()
    
    try:        
        
        form=employee.user_rate_form_set.last()
    
        if form.activation==1:
            notification_message="the Rating is availible now please Rating your team !"
            notifications.append(notification_message)
            hourse=form.Form_id.hours_expire
            date=form.date
            defrent=timezone.now()-date
            is_active=True
            obj_1=len(form.user_rate_set.all())
            obj_2=len(employee.get_staff())
            obj_3=len(form.Form_id.rating_form_set.all())
            if obj_3 * obj_2 <= obj_1:
                rate=user_rate(Rate_id=Rate.objects.get(id=5),employee_id=employee,note="You rate all the team ",value=18)
                rate.save()
                notifications.pop()
                notifications.append("You rate your team so you get some point")
                form.activation=-1
                form.save()
                
            if defrent.seconds//3600>=hourse:
                form.activation=0
                form.save()
                
                
        elif form.activation == 0:
            notification_message = "the Rating is not availible !"
            notifications.append(notification_message)
            form.activation =-1
            form.save()
            rate=user_rate(Rate_id=Rate.objects.get(id=5),employee_id=employee,note="You did no't Rate your all team",value=10)
            rate.save()
            notifications.append("You did no't Rate your all team you will loss some point")
            
            
                
        else:
            pass
            
    except Exception as ex:
        print(ex)
    
    notifications_len=len(notifications)
    context={'employee':employee,'rating_list':rating_list,"prise_List":prise_point,"color":random_color,"is_active":is_active,"notifications":notifications,"noti_len":notifications_len}
    return render(request,'Profile.html',context)


@login_required(login_url='login')
def view_point(request,emp_id):
    random_color=['success','danger','info','warning']
    employee=Employee.objects.get(id=emp_id)
    rating_list=list(employee.user_rate_set.all())
    rating_list=calculate_rating(rating_list)
    
    context={'employee':employee,'rating_list':rating_list,"color":random_color}
    return render(request,'point_view.html',context)


@login_required(login_url='login')
def complaint(request):
    employee=request.user.employee
    if request.method=='POST':
        note=request.POST.get('note')
        compl = Complaint(employee_id=employee,note=note)
        compl.save()
        return redirect('profile')
    
    rating_list=list(employee.user_rate_set.order_by('-id')[:10])
    context={"rating_list":rating_list}#,"form":form}
    return render(request,'complaint.html',context)
    



#to implement
@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def account_setting(request):
    employee=request.user.employee
    service=timezone.now()-employee.join_date
    update_form=UpdateProfile(instance=employee)
    if request.method=="POST":
        update_form=UpdateProfile(request.POST,request.FILES,instance=employee)
        if update_form.is_valid():
            update_form.save()
        
    context={"employee":employee,"form":update_form,"service":service}
    
    return render(request,'setting.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['employee'])
def boss_rating(request,emp_id):
    employee=Employee.objects.get(id=emp_id)
    permession_set=list(request.user.employee.user_rate_form_set.last().Form_id.rating_form_set.all())
    form_id=request.user.employee.user_rate_form_set.last()
    result=get_rating_data(permession_set)
    if request.method=='POST':
        for i in result:
            value=request.POST.get(i[1])
            note=request.POST.get(i[2])
            rate=user_rate(Rate_id=i[0],employee_id=employee,note=note,value=value,boss_form=form_id)
            rate.save()
    
        return redirect('profile')
    context={"permession_set":permession_set,"employee":employee}
    return render(request,'rating.html',context)



#admin section 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admin_profile(request):
    notifications=[]
    user_name=request.user.last_name
    users=Employee.objects.all()
    context={"noti_len":0,"notifications":notifications,"admin":user_name,"users":users}
    return render(request,'admin_profile.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def rating_details(request,emp_id):
    employee=Employee.objects.get(id=emp_id)
    rating_list=employee.user_rate_set.order_by('-id')
    context={"rating_list":rating_list,"employee":employee}#,"form":form}
    return render(request,'Rating_details.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit_rating(request,emp_id,rate_id):
    employee=Employee.objects.get(id=emp_id)
    rating_to_edit=employee.user_rate_set.get(id=rate_id)
    form=Edit_Rate(instance=rating_to_edit)
    if request.method=='POST':
        form=Edit_Rate(request.POST,request.FILES,instance=rating_to_edit)
        if form.is_valid():
            form.save()
            return redirect('Rating_details',emp_id)
        
    rate_type=rating_to_edit.Rate_id.rate_name
    context={"employee":employee,"form":form,"Rate_type":rate_type}#,"form":form}
    return render(request,'edit_user_rate.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit_employee(request,emp_id):
    empl=Employee.objects.get(id=emp_id)
    form=CreatEmployForm(instance=empl)
    if request.method=='POST':
        form=CreatEmployForm(request.POST,request.FILES,instance=empl)
        if form.is_valid():
            boss_id=request.POST['boss_id']
            boss_obj=Employee.objects.get(id=boss_id)
            level=boss_obj.level+1
            empl.level=level
            form.save()
            return redirect('admin_profile')
    context={"employee":empl,"form":form}
    return render(request,"edit_employee.html",context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_employee(request,emp_id):
    empl=Employee.objects.get(id=emp_id)
    form=CreatEmployForm(instance=empl)
    teams=empl.get_staff()
    worning=""
    if len(teams):
        worning="This User Hase some Employee who are Attached to him so be cerful if you dont move those user to right place thay will reconnect to the up level outomaticaly."
    if request.method=='POST':
        if len(teams):
            new_boss=empl.get_boss()
            for member in teams:
                member.boss_id.clear()
                member.boss_id.add(new_boss)
                member.level=new_boss.level+1
                member.save()
        user=empl.user        
        user.delete()    
        return redirect('admin_profile')
    context={"employee":empl,"form":form,"Note":worning}
    return render(request,"delete_employee.html",context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delet_rate(request,emp_id,rate_id):
    employee=Employee.objects.get(id=emp_id)
    rating_to_edit=employee.user_rate_set.get(id=rate_id)
    form=Edit_Rate(instance=rating_to_edit)
    if request.method == 'POST':
        rating_to_edit.delete()
        return redirect('Rating_details',emp_id)
    
    rate_type=rating_to_edit.Rate_id.rate_name
    context={"employee":employee,"form":form,"Rate_type":rate_type,}#,"form":form}
    return render(request,"delet_user_rate.html",context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admin_complaint(request):
    user_name=request.user.last_name
    complaint_list=Complaint.objects.order_by('-id')[:10]
    context={"complaint_list":complaint_list,"admin":user_name}
    return render(request,'admin_complaint.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Priz_viewing(request):
    random_color=['success','danger','info','warning']
    user_name=request.user.last_name
    prize=Price.objects.all()
    form = Priz_form()
    if request.method=='POST':
        form=Priz_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Priz')
    
    context={"Prize":prize,"color":random_color,"form":form,"admin":user_name}
    return render(request,'Prize.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit_prize(request,prize_id):
    prize=Price.objects.get(id=prize_id)
    form=Priz_form(instance=prize)
    if request.method=='POST':
        form=Priz_form(request.POST,request.FILES,instance=prize)
        if form.is_valid():
            form.save()
            return redirect('Priz')
    context={"Prize":prize,"form":form}
    return render(request,'edit_prize.html',context)
    
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_prize(request,prize_id):
    prize=Price.objects.get(id=prize_id)
    form=Priz_form(instance=prize)
    if request.method=='POST':
        prize.delete()
        return redirect('Priz')
    context={"Prize":prize,"form":form}
    return render(request,'delet_prize.html',context)
    
    
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admin_rate(request):
    random_color=['success','danger','info','warning']
    Rates=Rate.objects.all()
    user_name=request.user.last_name
    form = RateForm()
    if request.method=='POST':
        form=RateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_rate')
    
    context={"Rates":Rates,"color":random_color,"form":form,"admin":user_name}
    return render(request,'admin_rating.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def rating_edit(request,rate_id):
    rate=Rate.objects.get(id=rate_id)
    form=RateForm(instance=rate)
    if request.method=='POST':
        form=RateForm(request.POST,request.FILES,instance=rate)
        if form.is_valid():
            form.save()
            return redirect('admin_rate')
        else:
            messages.info(request,'The importance should be less than 10')
    context={"Rate":rate,"form":form}
    return render(request,'edit_rate.html',context)
    
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def rating_delete(request,rate_id):
    rate=Rate.objects.get(id=rate_id)
    form=RateForm(instance=rate)
    if request.method=='POST':
        rate.delete()
        return redirect('admin_rate')
    context={"Rate":rate,"form":form}
    return render(request,'delete_rate.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def rate_form(request):
    froms=Form.objects.all()
    user_name=request.user.last_name
    form=FormRateForm()
    if request.method=='POST':
        form=FormRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rate_form')
    
    context={"forms":froms,"form":form,"admin":user_name}
    return render(request,'RateForm.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit_form(request,form_id):
    form_obj=Form.objects.get(id=form_id)
    form=FormRateForm(instance=form_obj)
    Rates=Rate.objects.exclude(id=5)
    rates_ids=get_Rate_id(form_obj.rating_form_set.all())
    all_rate_ids=get_all_Rate_ids(Rates)
    if request.method=='POST':
        # if 'form_1' in request.POST:
        for rate_id in all_rate_ids:
            if str(rate_id) in request.POST and rate_id in rates_ids:
                pass
            elif  str(rate_id) not in request.POST and rate_id in rates_ids:
                obj=form_obj.rating_form_set.get(Rate_id_id=rate_id)
                obj.delete()
                
            else:
                rate_obj=Rate.objects.get(id=rate_id)
                obj=Rating_Form(Rate_id=rate_obj,form_id=form_obj)
                obj.save()
        form =FormRateForm(request.POST,request.FILES,instance=form_obj)
        if form.is_valid():
            form.save()
            return redirect('rate_form')
    context={"forms":form_obj,"form":form,"Rates":Rates,"Rate_ids":rates_ids}
    return render(request,'edit_form.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_form(request,form_id):
    form_to_edit=Form.objects.get(id=form_id)
    form=FormRateForm(instance=form_to_edit)
    if request.method=='POST':
        form_to_edit.delete()
        return redirect('rate_form')
    context={"forms":form_to_edit,"form":form}
    return render(request,'delete_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def User_Form(request):
    notifications=[]
    user_name=request.user.last_name
    users=[]
    for user in Employee.objects.all():
        if len(user.get_staff())!=0:
            try:
                form=user.user_rate_form_set.last()
                date=form.date
                diffrent=timezone.now()-date
                if diffrent.seconds//3600 >= 720:
                    users.append((user,True))
                else:
                    users.append((user,False))
            except:
                users.append((user,True))
            
    context={"noti_len":0,"notifications":notifications,"admin":user_name,"users":users}
    return render(request,'User_Form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def  add_user_form(request,emp_id):
    empl=Employee.objects.get(id=emp_id)
    forms=Form.objects.all()
    if request.method=='POST':
        form_id=request.POST['rate_form']
        form_obj=Form.objects.get(id=form_id)
        obj=User_Rate_Form(employee_id=empl,Form_id=form_obj)
        obj.save()
        return redirect('user_form')
    context={"employee":empl,"Forms":forms}
    return render(request,"Add_User_Form.html",context)
    