from operator import itemgetter
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timedelta
from django.utils import timezone
# Create your models here.


class Item(models.Model): 
    name=models.CharField(max_length=250)
    image=models.ImageField(upload_to='pics')
    description=models.CharField(max_length=50)  
    basePrice=models.PositiveIntegerField()
    currentPrice=models.PositiveIntegerField(default=0,blank=True,null=True)  
    tag=models.CharField(max_length=25)  
    status=models.BooleanField(default=False)  
    sold=models.CharField(max_length=10,default="unsold",blank=True,null=True)
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True,null=True)
    lowest_bidder_email=models.CharField(max_length=100,null=True,blank=True)
    lowest_bidder_id=models.PositiveIntegerField(null=True,blank=True)
    created_by =  models.ForeignKey(User, related_name='user_details', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, auto_now=True, null=True)


    def save(self, *args, **kwargs):
        if self.basePrice <0:
            self.basePrice=0
        
            
        super(Item, self).save(*args, **kwargs)


    def __str__(self):
        return "Lowest bidder for "+str(self. name)+" is "+str(self.lowest_bidder_email)


    


    # def save(self, *args, **kwargs):
    #     if self.created_by:
    #         User.objects.filter(username=self.user.username).update(is_staff=True)
             
    #     super(User_details, self).save(*args, **kwargs)
    



class User_details(models.Model):
    user =  models.ForeignKey(User, related_name='user_vendor', on_delete=models.CASCADE)
    name=models.CharField(max_length=250)
    mobile=models.PositiveIntegerField(blank=True,null=True)  
    is_Vendors=models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_Vendors:
            User.objects.filter(username=self.user.username).update(is_staff=True)
             
        super(User_details, self).save(*args, **kwargs)
    



class Bidder(models.Model):
    user =  models.ForeignKey(User, related_name='user_bidder', on_delete=models.CASCADE) 
    item =  models.ForeignKey(Item, related_name='bidder_item', on_delete=models.CASCADE)
    myPrice=models.PositiveIntegerField(blank=True,null=True)  
    contract_status=models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, auto_now=True, null=True)


    def save(self, *args, **kwargs):
        if int(self.myPrice )<0:
            self.myPrice=0
            
             
        super(Bidder, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.item.name)+"  "+str(self.myPrice)+" "+str(self.user.email)



