from models import *
import pdb
from django.db.models import Q


def get_matching_advertisements(search_query, logged_in_user):
    valid_ads = set()
    c1 = [x['user1_id'] for x in Circles.objects.values('user1_id').filter(user2_id=logged_in_user)];
    c2 = [x['user2_id'] for x in Circles.objects.values('user2_id').filter(user1_id=logged_in_user)];
    circles = c1 +c2;
    search_query = search_query.lower()
    itm_tps = Item_type.objects.all()
    for x in itm_tps:
        if search_query in x.item_name.lower():
            return Advertisement.objects.filter(item_type_id=x.item_id)
    words = search_query.split();
    all_adv = Ad_attr.objects.all();
    for adv in all_adv:
        for word in words:
            if word == adv.ad_attr_value.lower():
               if adv.advertisement_id.seller_id.user_id in circles:
                    valid_ads.add(adv.advertisement_id)
                    break;
    return valid_ads;


def get_matching_users(search_query):
    valid_users = []
    words = search_query.lower().split();
    all_users = Custom_user.objects.all();
    for usr in all_users:
        temp = set();
        temp.add(usr.first_name.lower());
        temp.add(usr.last_name.lower());
        if temp.issubset(set(words)):
            valid_users.insert(0, usr)
            continue;
        for word in words:
            if word == usr.first_name.lower() or word == usr.last_name.lower():
                valid_users.append(usr)
    return valid_users;
