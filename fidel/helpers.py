from fidel_app.models import *
from random import randint
from random import seed
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.models import User
import pdb
first_names = ["Naina","Rajeev","Ayush","Honey","Swapnil","Sankalp","Harshit","Vikas","Utkarsh","Naman","Harshad","Medha","Swapnali","Prikshit","Prakhar","Imroj","Rahul","Abhinav","Harsimran"];
last_names = ["Bansal","Kumar","Bagla","Singla","Godbole","Maurya","Kumar","Almal","Barnwal","Chabra","Rana","Gupta","Futane","Gera","Asthana","Qamar","Jha","Puri","Singh"]
cities = ["Ropar","Chandigarh","Bahadurgarh","Delhi","Bhopal","Kanpur","Cheema","Hyderabad","Gurgaon"]
item_types = ["Mobile","Television","Laptop","Book","Sport","Car","Bike","Cycle"]
attributes = ["Brand","Model","Camera","Ram","Screen_size","Hard_disk","Author","Publisher","Engine_details","Operating_system","Title","ISBN"]
item_att_value={};
item_att_value["Ram"]=["0.5 GB","1 GB","2 GB","4 GB"];
item_att_value["Brand"]=["Samsung","Apple","Micromax","Adidas"];
item_att_value["Camera"]=["2 MP","5 MP","8 MP"];
item_att_value["Hard_disk"]=["256 GB","512 GB","1024 GB"];
item_att_value["Operating_system"] = ["Apple","Linux","Android","Windows"]
unique_email_ids =[];
unique_phone_numbers = [];

item_att ={};
item_att["Mobile"]=["Brand","Model","Camera","Ram"];
item_att["Television"]=["Brand","Model","Screen_size"];
item_att["Laptop"]=["Brand","Model","Ram","Hard_disk"];
item_att["Book"]=["Title","Author","Publisher","ISBN"];
item_att["Sport"]=["Brand","Model"];
item_att["Car"] = ["Brand","Model","Engine_details"];
item_att["Bike"] = ["Brand","Model","Engine_details"];
item_att["Cycle"] = ["Brand","Model"]
def generateRandomString(n):
	temp =  "abcdefghijklmnopqrstuvwxyz";
	output = "";
	for x in range(n):
		output = output+temp[randint(0,25)]
	return output

def createUser():
	size =len(first_names)
	first_name = first_names[randint(0,size-1)];
	last_name = last_names[randint(0,size-1)];
	email_id = generateRandomString(9)+"@gmail.com";
	while email_id in unique_email_ids:
		email_id = generateRandomString(9)+"@gmail.com";
	unique_email_ids.append(email_id);
	passw = generateRandomString(8);
	street_name = generateRandomString(9);
	house_number = generateRandomString(2)+"-"+str(randint(1,1000));
	size = len(cities);
	city = cities[randint(0,size-1)];
	pin_code = randint(100000,999999);
	user = User.objects.create_user(email_id,email_id, passw);
	user.save();
	b = Custom_user(first_name=first_name,last_name=last_name,email_id=email_id,password=passw,street_name=street_name,house_number=house_number,city=city,pin_code=pin_code);
	b.save();


def createPhone():
	for x in unique_email_ids:
		print x
		b = Custom_user.objects.get(email_id=x);
		r = randint(1,2);
		while r==1:
			p = randint(1000000,9999999999)
			while p in unique_phone_numbers:
				p = randint(1000000,9999999999);
			unique_phone_numbers.append(p);
			temp = User_phone_number(user_id=b,phone_number=str(p));
			temp.save();
			r=randint(1,2);

def createConnectionsAndPendingRequests():
	size = len(unique_email_ids);
	for x in range(size):
		for y in range(x+1,size):
			user1 = Custom_user.objects.get(email_id=unique_email_ids[x]);
			user2 = Custom_user.objects.get(email_id=unique_email_ids[y]);
			r = randint(1,6);
			if( r==1):
				temp = Connected_to(user1=user1,user2=user2);
				temp.save();
			elif(r==2):
				temp = Pending_request(sender_id=user1,receiver_id=user2);
				temp.save();

def createItemType():
	for x in item_types:
		temp = Item_type(item_name=x);
		temp.save();

def createAttribute():
	for x in attributes:
		temp = Attribute(attribute_name=x);
		temp.save();

def createItemAttribute():
	for item_type in item_att.keys():
		atts = item_att[item_type]
		t1 = Item_type.objects.get(item_name=item_type);

		for att in atts:
			t2= Attribute.objects.get(attribute_name=att);
			if(item_att_value.get(att)):
				for x in item_att_value[att]:
					b = Item_attribute(item_type_id=t1,attribute_id=t2,attribute_value=x);
					b.save();
			else:
				b = Item_attribute(item_type_id=t1,attribute_id=t2);
				b.save();

def getAttVal(att_name):
	return generateRandomString(6);

def createAdvertisements():
	for em_id in unique_email_ids:
		#pdb.set_trace();
		user = Custom_user.objects.get(email_id=em_id)
		num_ads = randint(0,4)
		for y in range(num_ads):
			price = randint(1,10000);
			Original_price = randint(price+1,5*price)
			period_of_use = randint(0,200)
			l = len(item_types);
			x = randint(1,l);
			item_name = item_types[x-1];
			item_type = Item_type.objects.get(item_name=item_name);
			timestamp = datetime.now();
			b = Advertisement(seller_id=user,price=price,item_type_id=item_type,original_price=Original_price,period_of_use=period_of_use,timestamp=timestamp)
			b.save();
			for z in item_att[item_name]:
				att_id = Attribute.objects.get(attribute_name=z);
				if(item_att_value.get(z)):
					temp = item_att_value[z];
					value = temp[randint(0,len(temp)-1)];
				else:
					value = getAttVal(z);
				temp = Ad_attr(advertisement_id=b,attribute_id=att_id,ad_attr_value=value);
				temp.save();

def createRequirements():
	for em_id in unique_email_ids:
		user = Custom_user.objects.get(email_id=em_id)
		num_ads = randint(0,4)
		for y in range(num_ads):
			price = randint(1,10000);
			Original_price = randint(price+1,5*price)
			period_of_use = randint(0,200)
			l = len(item_types);
			x = randint(1,l);
			item_name = item_types[x-1];
			item_type = Item_type.objects.get(item_name=item_name);
			b = Requirement(buyer_id=user,max_price=price,item_type_id=item_type,max_period_of_use=period_of_use)
			b.save()
			for z in item_att[item_name]:
				att_id = Attribute.objects.get(attribute_name=z);
				value = getAttVal(z);
				temp = Req_attr(requirement_id=b,attribute_id=att_id,req_attr_value=value);
				temp.save();


def createAdvertisementNotification():
	num_notifications=1000;
	usrs  = Custom_user.objects.all();
	advts = Advertisement.objects.all();
	n1 = len(usrs);
	n2 = len(advts);
	for x in range(num_notifications):
		t1 = randint(0,n1-1);
		t2 = randint(0,n2-1);
		t = datetime.now();
		try:
			b = Advertisement_notification(user_id=usrs[t1],advertisement_id=advts[t2],timestamp=t);
			b.save();
		except:
			pass

def PopulateDatabase():
	User.objects.all().delete()
	Custom_user.objects.all().delete()
	User_phone_number.objects.all().delete()
	Pending_request.objects.all().delete()
	Connected_to.objects.all().delete()
	Message.objects.all().delete()
	Item_type.objects.all().delete()
	Attribute.objects.all().delete()
	Item_attribute.objects.all().delete()
	Advertisement.objects.all().delete()
	Advertisement_pictures.objects.all().delete()
	Ad_attr.objects.all().delete()
	Requirement.objects.all().delete()
	Req_attr.objects.all().delete()
	Advertisement_notification.objects.all().delete()
	Connected_notification.objects.all().delete()
	numUsers = 100;
	seed(1)
	for x in range(numUsers):
		createUser();
	createPhone();
	createConnectionsAndPendingRequests();
	createItemType();
	createAttribute();
	createItemAttribute();
	createAdvertisements();
	createRequirements();
	createAdvertisementNotification();
