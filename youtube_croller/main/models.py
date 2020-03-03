from django.db import models

# Create your models here.

class Search(models.Model):
    search = models.CharField(max_length = 20)

class Youtube_result(models.Model):
    channel_name = models.CharField(max_length = 100)
    subscriber_num =  models.FloatField() 
    not_int_subscriber_num = models.CharField(max_length = 100)
    profile_url = models.CharField(max_length = 100)

class Instagram_result(models.Model):
    insta_id = models.CharField(max_length=50)
    profile_url = models.CharField(max_length=100)

class Contract(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

class Record(models.Model):
    contract = models.ForeignKey(Contract,on_delete=models.CASCADE)
    insta_id = models.CharField(max_length=30)
    influencer = models.CharField(max_length=30)
    #바꾸기 귀찮아서 안바꿈 feed_condition아니라  DM내용임
    feed_condition = models.TextField(max_length=1000)
    is_confirmed = models.BooleanField()