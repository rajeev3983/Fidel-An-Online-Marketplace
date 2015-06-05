from django.conf.urls import patterns, include, url
from django.contrib import admin
from fidel_app import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fidel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.home),
    
    #login urls
	url(r'^login/',views.login),
	url(r'^login_auth/',views.login_auth),
	url(r'^logout/',views.logout),
	url(r'^logged_in/',views.logged_in),
	url(r'^invalid_login/',views.invalid_login),
	
	url(r'^signup/',views.signup),
	url(r'^signup_success/',views.signup_success),
	
	url(r'^myprofile/',views.view_my_profile),
	url(r'^delete_my_profile/',views.delete_my_profile),
	url(r'^edit_my_profile/',views.edit_my_profile),
	url(r'^edit_my_profile_next/',views.edit_my_profile_next),
	
	url(r'^advertisements/',views.view_my_advertisement),
	url(r'^create_advertisement/',views.create_advertisement),
	url(r'^delete_advertisement/',views.delete_advertisement),
	url(r'^form_attributes/',views.form_attributes),
	url(r'^requirements/',views.view_my_requirement),
	url(r'^create_requirement/',views.create_requirement),
	url(r'^delete_requirement/',views.delete_requirement),
	url(r'^search/',views.search),
    url(r'^items/',views.filter_advertisements),
	url(r'^requests/',views.requests),
	url(r'^notifications/',views.notifications),
	url(r'^messages/',views.messages),
	url(r'^show_message/',views.show_message),
	url(r'^add_message/',views.add_message),
	url(r'^users/',views.user_profile),
	url(r'^show_advertisement/',views.show_advertisement),
    url(r'^add_to_pending_requests/', views.add_to_pending_requests),
)
