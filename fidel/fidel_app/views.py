from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import *
from models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime
from django.forms.formsets import formset_factory
import pdb
import utils
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.formsets import formset_factory
# from models import EmailAuth
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
import json
from django.core import serializers
# Create your views here.


def home(request):
    if ( not request.user ) or ( not request.user.is_authenticated() ):
        return HttpResponseRedirect('/login/');
    dict = {};
    item_types = Item_type.objects.all()
    dict['item_names'] = [item.item_name for item in item_types];
    return render_to_response('home.html', dict);


def login(request):
    if request.user and request.user.is_authenticated():
        return HttpResponseRedirect('/')
    c = {};
    c.update(csrf(request));
    return render_to_response('login.html', c);


def login_auth(request):
    email_id = request.POST.get('email_id', '');
    password = request.POST.get('password', '');
    user = auth.authenticate(username=email_id, password=password);
    print email_id, password;
    #pdb.set_trace();
    if user is not None:
        auth.login(request, user);
        return HttpResponseRedirect('/');
    else:
        return HttpResponseRedirect('/invalid_login/');


def logout(request):
    auth.logout(request);
    return HttpResponseRedirect('/');


def logged_in(request):
    return render(request, 'logged_in.html');


def invalid_login(request):
    return render(request, 'login.html');

@csrf_exempt
def signup(request):
	#Image_form_set = formset_factory(UploadImageForm);
	if request.method == 'POST':
		#form = SignupForm(request.POST, request.FILES);
		user = User.objects.create_user(request.POST.get('email_id'), request.POST.get('email_id'), request.POST.get('password'));
		user.save();
		'''print form.is_valid(), form.errors;
		if form.is_valid():
        
        #image_form_set = Image_form_set(request.POST, request.FILES);
		#if form.is_valid() and image_form_set.is_valid():
			#form.profile_picture = request.FILES.get('profile_picture')
			
			form.save();'''
		user=Custom_user.objects.create(email_id=request.user.username);
		
		user.first_name = request.POST.get('first_name');
		user.last_name = request.POST.get('last_name');
		user.email_id = request.POST.get('email_id');
		user.password = request.POST.get('password');
		user.street_name = request.POST.get('street_name');
		user.house_number = request.POST.get('house_number');
		user.city = request.POST.get('city');
		user.pin_code = request.POST.get('pin_code');
		user.profile_picture = request.FILES.get('profile_picture');
		
		user.save();
				
		#print request.POST.getlist('phone[]');
		for phone_num in request.POST.getlist('phone[]'):
			phone_num_object=User_phone_number.objects.create(phone_number=phone_num, user_id_id=user.user_id);
			phone_num_object.save();		
		return HttpResponseRedirect('/signup_success/');
	'''args = {}
	args.update(csrf(request));
	args['form'] = SignupForm();
	return render_to_response('signup.html', args);'''
	return render_to_response('signup.html');


def signup_success(request):
    return render_to_response('signup_success.html');


def view_my_profile(request):
	user1 = Custom_user.objects.get(email_id=request.user.username)
	args = {'user1':user1, 'user1_phone_num': User_phone_number.objects.filter(user_id_id=user1.user_id)}
	return render_to_response('user_profile.html', args);

def show_advertisement(request):
    #pdb.set_trace()
    dict= {};
    if request.method == 'GET':
        ad_id=request.GET['ad_id'];
        valid_ads=Advertisement.objects.filter(advertisement_id=ad_id);
        dict= {};
        advts = [];
        for x in valid_ads:
            temp = {};
            temp['advertisement_id']=x.advertisement_id;
            temp['item_type']=x.item_type_id.item_name;
            temp['price']=x.price;
            temp['original_price']=x.original_price;
            temp['period_of_use']=x.period_of_use;
            temp['seller_name']= x.seller_id.first_name+" "+x.seller_id.last_name
            temp['seller_id']=x.seller_id.user_id;
            attributes = Ad_attr.objects.filter(advertisement_id=x.advertisement_id);
            attr_dict={}
            for y in attributes:
                attr_dict[y.attribute_id.attribute_name]=y.ad_attr_value;
            temp['attr_dict']=attr_dict;
            advts.append(temp)
            dict['advts']=advts;
        if( len(advts)==0):
            dict['no_add']="This advertisement does not exist.";       
    return render_to_response('advertisement.html',dict);

@csrf_exempt
def edit_my_profile(request):
	user1 = Custom_user.objects.get(email_id=request.user.username)
	args = {'user1':user1, 'user1_phone_num': User_phone_number.objects.filter(user_id_id=user1.user_id)}
	return render_to_response('edit_profile.html', args);

@csrf_exempt
def edit_my_profile_next(request):
	user=Custom_user.objects.get(email_id=request.user.username);
	print (request.POST.getlist('phone_num[]'));
	#user(email_id = request.POST.get('email_id'), first_name = request.POST.get('first_name'), last_name = request.POST.get('last_name'));
	#print "pic", request.POST.get('profile_picture');
	user.first_name = request.POST.get('first_name');
	user.last_name = request.POST.get('last_name');
	user.email_id = request.POST.get('email_id');
	user.password = request.POST.get('password');
	user.street_name = request.POST.get('street_name');
	user.house_number = request.POST.get('house_number');
	user.city = request.POST.get('city');
	user.pin_code = request.POST.get('pin_code');
	user.profile_picture = request.FILES.get('profile_picture');
	
	user.save();
	if(request.POST.getlist('phone[]')[0]):
		for phone_no in request.POST.getlist('phone[]'):
				phone_num_object=User_phone_number.objects.create(phone_number=phone_no, user_id_id=user.user_id);
				phone_num_object.save();	
	return HttpResponseRedirect('/');

@csrf_exempt
def delete_my_profile(request):
	user=Custom_user.objects.get(email_id=request.user.username)
	User_phone_number.objects.filter(user_id_id=user.user_id)
	User.objects.filter(username=request.user.username).delete();
	Custom_user.objects.filter(email_id=request.user.username).delete();

	return render_to_response('login.html');

def view_my_advertisement(request):
    #pdb.set_trace()
    dict= {};
    user = Custom_user.objects.get(email_id=request.user.email);
    valid_ads=Advertisement.objects.filter(seller_id=user.user_id);
    advts = [];
    for x in valid_ads:
        temp = {};
        temp['advertisement_id']=x.advertisement_id;
        temp['item_type']=x.item_type_id.item_name;
        temp['price']=x.price;
        temp['original_price']=x.original_price;
        temp['period_of_use']=x.period_of_use;
        temp['seller_name']= x.seller_id.first_name+"    "+x.seller_id.last_name
        temp['seller_id']=x.seller_id.user_id;
        attributes = Ad_attr.objects.filter(advertisement_id=x.advertisement_id);
        pictures = Advertisement_pictures.objects.filter(advertisement_id=x.advertisement_id);
        attr_dict={}
        pict_dict={}
        for y in attributes:
            attr_dict[y.attribute_id.attribute_name]=y.ad_attr_value;
        pict_count = 0;
        for y in pictures:        
            pict_dict["image_"+str(pict_count)]=y.picture;
            pict_count=pict_count+1;
        temp['attr_dict']=attr_dict;
        temp['pict_dict']=pict_dict;
        advts.append(temp)
    dict['advts']=advts;
    if( len(advts)==0):
        dict['no_add']=user.first_name + ", you have not posted any advertisements yet!";
    return render_to_response('advertisements.html',dict);


def create_advertisement(request):
    Image_form_set = formset_factory(UploadImageForm);
    if request.method == 'POST':        
        form = CreateAdvertisementForm(request.POST);
        image_form_set = Image_form_set(request.POST, request.FILES);
        #pdb.set_trace()        
        if form.is_valid() and image_form_set.is_valid():
            user = Custom_user.objects.get(email_id=request.user.email);
            item_type = Item_type.objects.get(item_name=str(form.cleaned_data['item_type']));
            attribute = Attribute.objects.filter(item_attribute__item_type_id=item_type.item_id);
            ad = Advertisement(price=form.cleaned_data['price'],original_price=form.cleaned_data['original_price'],period_of_use=form.cleaned_data['period_of_use'],timestamp=datetime.now(),item_type_id_id=item_type.item_id,seller_id_id=user.user_id);
            #pdb.set_trace()
            ad.save();
            req_ids = set(Req_attr.objects.all().values_list('requirement_id', flat=True).distinct())
            for attr in attribute:
                if request.POST.get(attr.attribute_name):       
                    ad_attr = Ad_attr(ad_attr_value=request.POST[attr.attribute_name], advertisement_id_id=ad.advertisement_id, attribute_id_id=attr.attribute_id);
                    ad_attr.save();
                    req_id = Req_attr.objects.filter(req_attr_value=request.POST[attr.attribute_name], attribute_id_id=attr.attribute_id).values_list('requirement_id', flat=True).distinct()
                    req_ids = req_ids.intersection(req_id)
            no_image = True;
            for i in range(0,image_form_set.total_form_count()):
                key = 'form-'+str(i)+'-image'
                if key in request.FILES:
                    no_image=False;
                    file = request.FILES[key];
                    filename = str(a.advertisement_id) + '_' +  str(i) + '_' +str(file._get_name());
                    ad_pict = Advertisement_pictures(advertisement_id_id=ad.advertisement_id, picture=filename);
                    ad_pict.save();
                    handle_uploaded_file(file, filename);
            match_req = Requirement.objects.filter(item_type_id_id=item_type.item_id)
            match_req = match_req.filter(requirement_id__in=req_ids)
            if form.cleaned_data['price']>0:
                match_req = match_req.filter(max_price__gte=form.cleaned_data['price'])
            if form.cleaned_data['period_of_use']>0:
                match_req = match_req.filter(max_period_of_use__gte=form.cleaned_data['period_of_use'])
            for req in match_req:
                an = Advertisement_notification(advertisement_id_id=ad.advertisement_id, user_id_id=req.buyer_id_id, timestamp=timezone.now())
                an.save()
            if no_image:
                ad_pict = Advertisement_pictures(advertisement_id_id=ad.advertisement_id, picture="NoImage.jpg");
                ad_pict.save();
            return HttpResponseRedirect('/');    
    else:
        form = CreateAdvertisementForm();
        image_form_set = Image_form_set();
    args = {}
    args.update(csrf(request));
    args['form'] = form;    
    args['image_form_set'] = image_form_set;
    return render_to_response('create_advertisement.html', args);

def delete_advertisement(request):
    if request.method == 'GET':        
        ad_id=request.GET['ad_id'];
        ad = Advertisement.objects.get(advertisement_id=ad_id);
        ad.delete();
    return HttpResponseRedirect('/advertisements/');

def form_attributes(request):
    data = {};
    if request.method == 'GET':
        cat = request.GET['category'];
        item_type = Item_type.objects.get(item_name=cat);
        attribute = Attribute.objects.order_by().filter(item_attribute__item_type_id=item_type.item_id).distinct();
        attr = [ str(i.attribute_name) for i in attribute ];
        data['attr'] = attr;
        item_type_name = request.GET['category'];    
        attr = [];    
        item_type = Item_type.objects.get(item_name=item_type_name);    
        attribute = Attribute.objects.order_by().filter(item_attribute__item_type_id=item_type.item_id).distinct();
        fld = "";
        for a in attribute:
            domain=Item_attribute.objects.values('attribute_value').filter(attribute_id_id=a.attribute_id, item_type_id_id=item_type.item_id);
            if domain.count() > 1:
                fld = fld + '<tr id ="row_'+a.attribute_name+'"><td><label class=\"control-label\">'+a.attribute_name+'</label></td><td>';
                for d in domain:
                    #pdb.set_trace();
                    fld = fld + '<input type=\"radio\" name="'+a.attribute_name+'" value="'+d['attribute_value']+'">'+d['attribute_value']+'&nbsp;&nbsp;&nbsp;&nbsp;'
                fld = fld + "</td></tr>";
            else:
                
                fld = fld + '<tr id ="row_'+a.attribute_name+'"><td><label class="control-label" for="id_'+a.attribute_name+'">'+a.attribute_name+'</label"></td><td><input type="text" name="'+a.attribute_name+'" id="id_'+a.attribute_name+'"></td></tr>'
    #pdb.set_trace();  
    #return JsonResponse(fld, safe=False);
    return HttpResponse(fld, content_type="text/html");


def view_my_requirement(request):
    dict= {};
    user = Custom_user.objects.get(email_id=request.user.email);
    valid_reqs=Requirement.objects.filter(buyer_id=user.user_id);
    reqs = [];
    for x in valid_reqs:
        temp = {};
        temp['requirement_id']=x.requirement_id;
        temp['item_type_id']=x.item_type_id;
        temp['buyer_id']=x.buyer_id;
        temp['item_type']=x.item_type_id.item_name;
        temp['max_price']=x.max_price;
        temp['max_period_of_use']=x.max_period_of_use;
        attributes = Req_attr.objects.filter(requirement_id=x.requirement_id);
        attr_dict={}
        for y in attributes:
            attr_dict[y.attribute_id.attribute_name]=y.req_attr_value;
        temp['attr_dict']=attr_dict;
        reqs.append(temp)
    dict['reqs']=reqs;
    if( len(reqs)==0):
        dict['no_add']=user.first_name + ", you have not posted any requirements yet!";
    return render_to_response('requirements.html',dict);


def create_requirement(request):
    if request.method == 'POST':        
        form = CreateRequirementForm(request.POST);
        if form.is_valid():
            
            user = Custom_user.objects.get(email_id=request.user.email);
            item_type = Item_type.objects.get(item_name=str(form.cleaned_data['item_type']));
            attribute = Attribute.objects.order_by().filter(item_attribute__item_type_id=item_type.item_id).distinct();            
            a = Requirement(max_price=form.cleaned_data['max_price'],max_period_of_use=form.cleaned_data['max_period_of_use'],item_type_id_id=item_type.item_id,buyer_id_id=user.user_id);
            #pdb.set_trace()
            a.save();
            #pdb.set_trace();
            for attr in attribute:                
                req_attr = Req_attr(req_attr_value=request.POST[attr.attribute_name], requirement_id_id=a.requirement_id, attribute_id_id=attr.attribute_id);
                req_attr.save();
            return HttpResponseRedirect('/');    
    else:
        form = CreateRequirementForm();
    args = {}
    args.update(csrf(request));
    args['form'] = form;
    return render_to_response('create_requirement.html', args);

def delete_requirement(request):
    if request.method == 'GET':        
        req_id=request.GET['req_id'];
        req = Requirement.objects.get(requirement_id=req_id);
        req.delete();
    return HttpResponseRedirect('/requirements/');


def search(request):
    logged_in_user = Custom_user.objects.get(email_id=request.user.email);
    dict = {};
    search_query = request.GET['q'];
    dict['q'] = search_query;
    valid_ads = utils.get_matching_advertisements(search_query,logged_in_user);
    advts = [];
    for x in valid_ads:
        temp = {};
        temp['advertisement_id'] = x.advertisement_id;
        temp['item_type'] = x.item_type_id.item_name;
        temp['price'] = x.price;
        temp['original_price'] = x.original_price;
        temp['period_of_use'] = x.period_of_use;
        temp['seller_name'] = x.seller_id.first_name + " " + x.seller_id.last_name
        temp['seller_id'] = x.seller_id.user_id;
        attributes = Ad_attr.objects.filter(advertisement_id=x.advertisement_id);
        attr_dict = {}
        for y in attributes:
            attr_dict[y.attribute_id.attribute_name] = y.ad_attr_value;
        temp['attr_dict'] = attr_dict;
        advts.append(temp)
    dict['advts'] = advts;
    if ( len(advts) == 0):
        dict['no_add'] = "No Advertisement found";
    valid_users = utils.get_matching_users(search_query)
    usrs = []
    for x in valid_users:
        temp = {}
        temp['user_id'] = x.user_id;
        temp['name'] = x.first_name + " " + x.last_name;
        temp['city'] = x.city;
        usrs.append(temp);
    dict['usrs'] = usrs;
    if ( len(usrs) == 0):
        dict['no_usrs'] = "Your search did not match any person"
    return render_to_response('search_results.html', dict);


def requests(request):
    usr_email = request.user.email;
    usr = Custom_user.objects.get(email_id=usr_email);
    pending_requests = Pending_request.objects.filter(receiver_id=usr);
    args = {'requests': pending_requests, 'logged_in_user': usr.user_id};
    return render_to_response("pending_requests.html", args);

def notifications(request):
    usr = Custom_user.objects.get(email_id=request.user.email)
    adv_notifications = Advertisement_notification.objects.filter(user_id=usr).order_by('-timestamp')
    conn_notifications = Connected_notification.objects.filter(sender_id=usr).order_by('-timestamp')
    #pdb.set_trace();
    dict = {};
    n = len(adv_notifications);
    m = len(conn_notifications);
    p1=0;p2=0;
    notification_list=[];
    while p1<n and p2<m :
        if( adv_notifications[p1].timestamp>conn_notifications[p2].timestamp):
            temp ={};
            adv = adv_notifications[p1].advertisement_id;
            temp['notifi']=adv.seller_id.first_name+" "+adv.seller_id.last_name+" posted an advertisment which matches your requirement";
            temp['link']= "/show_advertisement?id="+str(adv_notifications[p1].advertisement_id.advertisement_id);            
            notification_list.append(temp);
            p1+=1;
        else:
            temp ={}
            receiver = conn_notifications[p2].receiver_id;
            temp['notifi'] = receiver.first_name+" "+receiver.last_name+" accepted your connection request";
            temp['link']="users/?user_id="+str(receiver.user_id);
            notification_list.append(temp)
            p2+=1;
    while p1<n:
            temp ={};
            adv = adv_notifications[p1].advertisement_id;
            temp['notifi']=adv.seller_id.first_name+" "+adv.seller_id.last_name+" posted an advertisment which matches your requirement";
            temp['link']= "/show_advertisement?id="+str(adv_notifications[p1].advertisement_id.advertisement_id);            
            notification_list.append(temp);
            p1+=1;
    while p2<m:
            temp ={}
            receiver = conn_notifications[p2].receiver_id;
            temp['notifi'] = receiver.first_name+" "+receiver.last_name+" accepted your connection request";
            temp['link']="users/?user_id="+str(receiver.user_id);
            notification_list.append(temp)
            p2+=1;
    dict['notifications']=notification_list;
    if(len(notification_list)==0):
	    dict['invalid']='No notification found';
    return render_to_response('notifications.html',dict);


def messages(request):
    cur_user = get_object_or_404(Custom_user, email_id=request.user.username)
    #cur_user = 422
    res = request.GET.get('show_message',0)
    conns_1 = Circles.objects.values('user1_id','user2_id').filter(user1_id=cur_user)
    conns_1 = Custom_user.objects.filter(user_id__in=[i['user2_id'] for i in conns_1])
    conns_2 = Circles.objects.values('user1_id','user2_id').filter(user2_id=cur_user)
    conns_2 = Custom_user.objects.filter(user_id__in=[i['user1_id'] for i in conns_2])
    dict = {'conns1':conns_1 , 'conns2':conns_2, 'res': res}
    return render(request, 'message.html', dict)

@csrf_exempt
def add_message(request):
    if request.method == 'POST':
        msg_text = request.POST['msg']
        sen_id = Custom_user.objects.get(email_id=request.user.username).user_id
        rec_id = int(request.POST['receiver_id'])
        ts = timezone.now()
        m = Message(message=msg_text, user1_id=sen_id, user2_id=rec_id, timestamp=ts)
        m.save()
        # return HttpResponse(
        #     json.dumps(response_data),
        #     content_type="application/json"
        # )
        return JsonResponse({'result':"success"})
    else:
        JsonResponse({'result':"Nothing to see"})
        # return HttpResponse(
        #     json.dumps({"Nothing to see"}),
        #     content_type="application/json"
        # )

@csrf_exempt
def show_message(request):
    if request.method == 'POST':
        #cur_user = 422
        #othr_user = 423
        cur_user = Custom_user.objects.get(email_id=request.user.username).user_id
        othr_user = int(request.POST['other_user'])
        msg = Message.objects.filter((Q(user1_id=cur_user) & Q(user2_id=othr_user)) | (Q(user2_id=cur_user) & Q(user1_id=othr_user))).order_by('-timestamp')
        
        #response_data = {}
        #response_data['msgs'] = msg
        #JsonResponse({'msgs':msg})
        dict = {'msgs':msg, 'other_user': othr_user}
        #return HttpResponse(json.dumps(msg), content_type="application/json")
        return render(request, 'show_message.html', dict)
    else:
        JsonResponse({'result':"Nothing to see"})
        # return HttpResponse(
        #     json.dumps({"Nothing to see"}),
        #     content_type="application/json"
        # )


def user_profile(request):
    user1 = Custom_user.objects.get(user_id=request.GET['user_id']);
    user2 = Custom_user.objects.get(email_id=request.user.username);
    degree = 0;
    pending_request = 0;

    if Pending_request.objects.filter(sender_id_id=user1.user_id, receiver_id_id=user2.user_id).exists():
        pending_request = 1;

    if Pending_request.objects.filter(sender_id_id=user2.user_id, receiver_id_id=user1.user_id).exists():
        pending_request = 2;

    if Connected_to.objects.filter(user1_id=min(user1.user_id, user2.user_id),
                                   user2_id=max(user1.user_id, user2.user_id)).exists():
        degree = 1;

    if DegreeTwo.objects.filter(user1_id=min(user1.user_id, user2.user_id),
                                user2_id=max(user1.user_id, user2.user_id)).exists():
        degree = 2;

    if DegreeThree.objects.filter(user1_id=min(user1.user_id, user2.user_id),
                                  user2_id=max(user1.user_id, user2.user_id)).exists():
        degree = 3;

    args = {'user2': user2, 'user1': user1, 'degree': degree, 'pending_request': pending_request, 'user1_phone_num': User_phone_number.objects.filter(user_id_id=user1.user_id)};
    return render_to_response('user_profile.html', args);


@csrf_exempt
def add_to_pending_requests(request):
    if request.POST['flag'] == '1':
        pending_request = Pending_request(sender_id_id=request.POST['sender_id'],
                                          receiver_id_id=request.POST['receiver_id']);
        pending_request.save();

    elif request.POST['flag'] == '2':
        Connected_to.objects.filter(user1_id=min(int(request.POST['sender_id']), int(request.POST['receiver_id'])),
                                    user2_id=max(int(request.POST['sender_id']),
                                                 int(request.POST['receiver_id']))).delete();

    elif request.POST['flag'] == '3':
        Pending_request.objects.filter(sender_id_id=request.POST['sender_id'],
                                       receiver_id_id=request.POST['receiver_id']).delete();
        connection = Connected_to(user1_id=min(int(request.POST['sender_id']), int(request.POST['receiver_id'])),
                                  user2_id=max(int(request.POST['sender_id']), int(request.POST['receiver_id'])));
        connection.save();
        Connected_notification(sender_id_id=request.POST['receiver_id'], receiver_id_id=request.POST['sender_id'], timestamp=timezone.now()).save()

    elif request.POST['flag'] == '4':
        Pending_request.objects.filter(sender_id_id=request.POST['sender_id'],
                                       receiver_id_id=request.POST['receiver_id']).delete();

    degree = 0;

    if Connected_to.objects.filter(user1_id=min(int(request.POST['sender_id']), int(request.POST['receiver_id'])),
                                   user2_id=max(int(request.POST['sender_id']),
                                                int(request.POST['receiver_id']))).exists():
        print 'hello';
        degree = 1;

    if DegreeTwo.objects.filter(user1_id=min(int(request.POST['sender_id']), int(request.POST['receiver_id'])),
                                user2_id=max(int(request.POST['sender_id']),
                                             int(request.POST['receiver_id']))).exists():
        degree = 2;

    if DegreeThree.objects.filter(user1_id=min(int(request.POST['sender_id']), int(request.POST['receiver_id'])),
                                  user2_id=max(int(request.POST['sender_id']),
                                               int(request.POST['receiver_id']))).exists():
        degree = 3;

    print degree
    return JsonResponse({'degree':degree});

def show_advertisement(request):
	adv_id = request.GET['id'];
	x = Advertisement.objects.get(advertisement_id=adv_id);
	dict = {}
	advts = [];
	temp = {};
	temp['advertisement_id'] = x.advertisement_id;
	temp['item_type'] = x.item_type_id.item_name;
	temp['price'] = x.price;
	temp['original_price'] = x.original_price;
	temp['period_of_use'] = x.period_of_use;
	temp['seller_name'] = x.seller_id.first_name + " " + x.seller_id.last_name
	temp['seller_id'] = x.seller_id.user_id;
	attributes = Ad_attr.objects.filter(advertisement_id=x.advertisement_id);
	attr_dict = {}
	for y in attributes:
		attr_dict[y.attribute_id.attribute_name] = y.ad_attr_value;
	temp['attr_dict'] = attr_dict;
	advts.append(temp)
	dict['advts'] = advts;
	return render_to_response('view_advertisement.html',dict);

@csrf_exempt
def filter_advertisements(request):
    dict = {};
    dict['Item_type']=Item_type.objects.all();
    if request.method == "POST":
        item_type_name=request.POST["item_type"];
        item_type = Item_type.objects.get(item_name=item_type_name);
        attribute = Attribute.objects.order_by().filter(item_attribute__item_type_id=item_type.item_id).distinct();
        valid_ads=Advertisement.objects.filter(item_type_id_id=item_type.item_id);
        for a in attribute:
            #pdb.set_trace()
            if a.attribute_name in request.POST:
                vals = request.POST.getlist(a.attribute_name);
                ad_attr = Ad_attr.objects.filter(advertisement_id_id__in = valid_ads).filter(attribute_id_id=a.attribute_id, ad_attr_value__in=vals);
                valid_ads=valid_ads.filter(advertisement_id__in = [i.advertisement_id_id for i in ad_attr]);
    else:
        #pdb.set_trace()
        item_type_name = request.GET['item_type'];    
        attr = [];    
        item_type = Item_type.objects.get(item_name=item_type_name);    
        attribute = Attribute.objects.order_by().filter(item_attribute__item_type_id=item_type.item_id).distinct();
        for a in attribute:
            domain=Item_attribute.objects.values('attribute_value').filter(attribute_id_id=a.attribute_id, item_type_id_id=item_type.item_id);
            if domain.count() > 1:
                attr.append([a.attribute_name, domain]);
        dict['attr'] = attr;   
        #pdb.set_trace()
        valid_ads = Advertisement.objects.filter(item_type_id_id = item_type.item_id);
    advts = [];
    dict['item_type']=item_type_name;
    for x in valid_ads:
        temp = {};
        temp['advertisement_id'] = x.advertisement_id;
        temp['item_type'] = x.item_type_id.item_name;
        temp['price'] = x.price;
        temp['original_price'] = x.original_price;
        temp['period_of_use'] = x.period_of_use;
        temp['seller_name'] = x.seller_id.first_name + " " + x.seller_id.last_name
        temp['seller_id'] = x.seller_id.user_id;
        attributes = Ad_attr.objects.filter(advertisement_id=x.advertisement_id);
        pictures = Advertisement_pictures.objects.filter(advertisement_id=x.advertisement_id);
        attr_dict = {}
        pict_dict = {}
        for y in attributes:
            attr_dict[y.attribute_id.attribute_name] = y.ad_attr_value;
        pict_count = 0;
        for y in pictures:        
            pict_dict["image_"+str(pict_count)]=y.picture;
            pict_count = pict_count + 1;
        pict_dict["image_0"]="NoImage.jpg";
        temp['attr_dict']=attr_dict;
        temp['pict_dict']=pict_dict;
        advts.append(temp)
    dict['advts'] = advts;
    if ( len(advts) == 0):
        dict['no_add'] = "No Advertisement found";
        
    if request.method=="POST":
        return render(request,'filter_ad_list.html',dict)
    else:
        return render_to_response('filter_advertisements.html', dict);

def handle_uploaded_file(file, filename):
    #pdb.set_trace()
    MEDIA_ROOT = './fidel_app/static/fidel_app/images/';
    fd = open('%s/%s' % (MEDIA_ROOT, filename), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
