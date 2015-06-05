from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User, check_password


# Create your models here.
class Custom_user(models.Model):
	user_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=512)
	last_name = models.CharField(max_length=512)
	email_id = models.EmailField(max_length=512)
	password = models.CharField(max_length=512)
	street_name = models.CharField(max_length=512,null=True)
	house_number = models.CharField(max_length=512,null=True)
	city = models.CharField(max_length=512,null=True)
	pin_code = models.IntegerField(null=True)
	profile_picture = models.ImageField(upload_to='/media/',null=True, default = 'media/motivation1.jpeg')
	class Meta:
		db_table = 'custom_user'
	'''def authenticate(self, email_id = None, password = None):
		try:
			user = self.get(email_id = email_id)
			if  '''


'''class EmailAuth(object):
	def authenticate(self, email = None, password = None):
		user = User.objects.get(email = email, password = password);
		return user;'''


class User_phone_number(models.Model):
    user_id = models.ForeignKey(Custom_user)
    phone_number = models.CharField(max_length=512)

    class Meta:
        unique_together = (("user_id", "phone_number"),)
        db_table = 'user_phone_number'


class Pending_request(models.Model):
    sender_id = models.ForeignKey(Custom_user, related_name='pending_request_sender')
    receiver_id = models.ForeignKey(Custom_user, related_name='pending_request_receiver')

    class Meta:
        unique_together = (("sender_id", "receiver_id"),)
        db_table = 'pending_request'


class Connected_to(models.Model):
    user1 = models.ForeignKey(Custom_user, related_name='connected_to_user1')
    user2 = models.ForeignKey(Custom_user, related_name='connected_to_user2')

    class Meta:
        unique_together = (("user1", "user2"),)
        db_table = 'connected_to'

class DegreeTwo(models.Model):
    user1 = models.ForeignKey(Custom_user, related_name='degree_two_user1')
    user2 = models.ForeignKey(Custom_user, related_name='degree_two_user2')

    class Meta:
        db_table = 'degree_two'
        managed = False

class DegreeThree(models.Model):
    user1 = models.ForeignKey(Custom_user, related_name='degree_three_user1')
    user2 = models.ForeignKey(Custom_user, related_name='degree_three_user2')

    class Meta:
        db_table = 'degree_three'
        managed = False

class Circles(models.Model):
    user1 = models.ForeignKey(Custom_user, related_name='circles_user1')
    user2 = models.ForeignKey(Custom_user, related_name='circles_user2')

    class Meta:
        db_table = 'circles'
        managed = False

class Message(models.Model):
    user1 = models.ForeignKey(Custom_user, related_name='message_user1')
    user2 = models.ForeignKey(Custom_user, related_name='message_user2')
    message = models.CharField(max_length=512)
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = (("user1", "user2", "timestamp"),)
        db_table = 'message'


class Item_type(models.Model):
	item_id = models.AutoField(primary_key=True)
	item_name = models.CharField(max_length=512)
	class Meta:
		db_table = 'item_type'
	def __unicode__(self):              # __unicode__ on Python 2
		return self.item_name

class Attribute(models.Model):
	attribute_id = models.AutoField(primary_key=True)
	attribute_name = models.CharField(max_length=512)
	class Meta:
		db_table = 'attribute'
	def __unicode__(self):              # __unicode__ on Python 2
		return self.attribute_name

class Item_attribute(models.Model):
    item_type_id = models.ForeignKey(Item_type)
    attribute_id = models.ForeignKey(Attribute)
    attribute_value = models.CharField(max_length=512,null=True);
    class Meta:
        unique_together = (("item_type_id", "attribute_id", "attribute_value"),)
        db_table = 'Item_attribute'


class Advertisement(models.Model):
    advertisement_id = models.AutoField(primary_key=True)
    seller_id = models.ForeignKey(Custom_user)
    item_type_id = models.ForeignKey(Item_type)
    price = models.IntegerField()
    original_price = models.IntegerField(null=True)
    period_of_use = models.CharField(max_length=512)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'advertisement'


class Advertisement_pictures(models.Model):
    advertisement_id = models.ForeignKey(Advertisement)
    picture = models.ImageField()

    class Meta:
        unique_together = (("advertisement_id", "picture"))
        db_table = 'ad_pictures'


class Requirement(models.Model):
    requirement_id = models.AutoField(primary_key=True)
    buyer_id = models.ForeignKey(Custom_user)
    item_type_id = models.ForeignKey(Item_type)
    max_price = models.IntegerField()
    max_period_of_use = models.CharField(max_length=512)

    class Meta:
        db_table = 'requirement'


class Advertisement_notification(models.Model):
    user_id = models.ForeignKey(Custom_user)
    advertisement_id = models.ForeignKey(Advertisement)
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = (("user_id", "advertisement_id"))
        db_table = 'advertisement_notification'


class Connected_notification(models.Model):
    sender_id = models.ForeignKey(Custom_user, related_name='connected_to_sender')
    receiver_id = models.ForeignKey(Custom_user, related_name='connected_to_receiver')
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = (("sender_id", "receiver_id", "timestamp"),)
        db_table = 'connected_notification'


class Ad_attr(models.Model):
    advertisement_id = models.ForeignKey(Advertisement)
    attribute_id = models.ForeignKey(Attribute)
    ad_attr_value = models.CharField(max_length=512)

    class Meta:
        unique_together = (("advertisement_id", "attribute_id", 'ad_attr_value'))
        db_table = 'ad_attr'


class Req_attr(models.Model):
    requirement_id = models.ForeignKey(Requirement)
    attribute_id = models.ForeignKey(Attribute)
    req_attr_value = models.CharField(max_length=512)

    class Meta:
        unique_together = (("requirement_id", "attribute_id", "req_attr_value"),)
        db_table = 'req_attr'
