from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=-1)
    join_date = models.DateTimeField(auto_now_add=True,null=True)
    
    # field for active employee for make a rating is boolean field .
    is_active=models.BooleanField(default=True)
    
    EXPERIANCE_LEVEL=(
        ('Newbie','Newbie'),
        ('Pubil','Pubil'),
        ('Specialist','Specialist'),
        ('Expert','Expert'),
        (' Candidate Master ',' Candidate Master '),
        ('Master','Master'),
        ('Grandmaster','Grandmaster'),
        ('Legendary Grandmaster ','Legendary Grandmaster ')
        
    )
    rank_level=models.CharField(max_length=30,choices=EXPERIANCE_LEVEL,null=True)
    
    boss_id = models.ManyToManyField("self",symmetrical=False)

    img=models.ImageField(null=True,blank=True)
    
    
    def __str__(self):
        return (self.first_name+" "+self.last_name)
    
    
    def get_profile(self):
        return {"name":"{} {}".format(self.first_name,self.last_name),
                "email":self.email,
                "phone_number":self.phone_number,
                "rank_level":self.rank_level,
                
                "years_of_service":timezone.now()-self.join_date
                }
    
    def set_level(self):
        self.level=self.boss_id.first().level+1
        
    
    def get_staff(self):
        return Employee.objects.filter(level=self.level+1,boss_id=self.id)
    
    
    def get_boss(self):
        return self.boss_id.first()
    
    
    def get_staff_rate(self,id):
        q=self.get_staff()
        obj=q.filter(id=id).first()
        return obj.rating_set
    
    
    def get_collage(self):
        return Employee.objects.filter(level=self.level).exclude(id=self.id)
    
    
    def get_staff_work_day(self,id):
        q=self.get_my_staff()
        obj=q.filter(id=id).first()
        return obj.work_day_set
    
    
    def get_rating_set(self):
        return self.user_rate_set
    
    def get_user_prise_set(self):
        return self.user_price_set.all()
    
    def  get_permisions(self):
        return self.user_permession_set
    
    
    
    
        
class Rating(models.Model):
    RATE_CHOICE=(
        ('Achivemant','Achivement'),
        ('Boss_rate','Boss_rate'),
        ('Time_rate','Time_rate')
    )
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True,null=True)
    rate_type=models.CharField(max_length=12,choices=RATE_CHOICE)
    note=models.CharField(max_length=200,null=True)
    rate=models.IntegerField()
    
    def __str__(self):
        return str(self.employee_id)

class Work_day(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    houres=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.employee_id)
    

class Complaint(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    note = models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return Employee.objects.filter(id=self.employee_id_id).first().last_name


class Rate(models.Model):
    rate_name=models.CharField(max_length=50)
    max_value=models.IntegerField()
    importance = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(0)])
    
    def __str__(self):
        return self.rate_name

class Form(models.Model):
     name=models.CharField(max_length=30,null=True)
     hours_expire=models.IntegerField()
     is_active=models.BooleanField(default=True)
     
     def __str__(self):
        return self.name



class Rating_Form(models.Model):
     Rate_id=models.ForeignKey(Rate, on_delete=models.CASCADE,null=True)
     form_id=models.ForeignKey(Form,on_delete=models.CASCADE,null=True)
     
     def __str__(self):
        return self.form_id.name+":"+self.Rate_id.rate_name  


     
class User_Rate_Form(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True,null=True)
    is_active=models.BooleanField(default=True)
    activation=models.IntegerField(default=1)

    def __str__(self):
        return self.employee_id.last_name +":"+self.Form_id.name


    
class user_rate(models.Model):
    Rate_id = models.ForeignKey(Rate, on_delete=models.CASCADE)    
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True,null=True)
    note=models.CharField(max_length=200,null=True)
    value=models.IntegerField()
    boss_form=models.ForeignKey(User_Rate_Form,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return Employee.objects.filter(id=self.employee_id_id).first().last_name #+ Rate.objects.filter(id=self.Rate_id).rate_name


class user_permession(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)     
    # permession_id = models.ForeignKey(Permessions, on_delete=models.CASCADE)
    Rate_id=models.ForeignKey(Rate, on_delete=models.CASCADE)

    expire_time=models.DateTimeField()
     

    
class Price(models.Model):
    Price_name=models.CharField(max_length=50)
    HitPoint=models.IntegerField()
    is_active=models.BooleanField(default=True)
     
    def __str__(self):
        return self.Price_name
    

class user_Price(models.Model):
    Price_id = models.ForeignKey(Price, on_delete=models.CASCADE)    
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return Employee.objects.filter(id=self.employee_id_id).first().last_name #+ Rate.objects.filter(id=self.Rate_id).rate_name


    
class Notification(models.Model):
    name=models.CharField(max_length=30,null=True)
    message=models.CharField(max_length=30,null=True)
    
    def __str__(self):
        return self.name
     

class User_Notification(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)
    message=models.CharField(max_length=50,null=True)
    is_read=models.BooleanField(default=False,null=True)
    
    def __str__(self):
        return self.employee_id.last_name+":"+self.notification_id.name

    
class Global_Notification(models.Model):
    notification_id=models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read=models.BooleanField(default=False)
    
    def __str__(self):
        return self.notification_id.name

    

