from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import *
from django.forms import IntegerField, Textarea

			
		
class CreateAdvertisementForm(forms.ModelForm):
	item_type = forms.ModelChoiceField(label='Select Item type', queryset=Item_type.objects.all());
	period_of_use = forms.IntegerField();
	class Meta:
		model = Advertisement;
		exclude = ['seller_id', 'item_type_id', 'timestamp'];
		fields = ['item_type', 'price', 'original_price', 'period_of_use'];
	def save(self, commit = True):
		user = super(CreateRequirementForm, self).save(commit=False)
		if commit:
			user.save();
		print user;	
		return user;			

class CreateRequirementForm(forms.ModelForm):
	item_type = forms.ModelChoiceField(label='Select Item type', queryset=Item_type.objects.all())
	max_period_of_use = IntegerField();
	class Meta:
		model = Requirement;
		exclude = ['buyer_id', 'item_type_id'];
		fields = ['item_type', 'max_price', 'max_period_of_use'];
	def save(self, commit = True):
		user = super(CreateAdvertisementForm, self).save(commit=False)		
		if commit:
			user.save();
		print user;	
		return user;			
		
def validate_file_extension(value):
    if not value.name.endswith('.jpg'):
        raise ValidationError(u'Error message')

class UploadImageForm(forms.Form):
    image = forms.ImageField(required=False,validators=[validate_file_extension])
    def save(self, commit = True):
        user = super(SignupForm, self).save(commit=False)
        if commit:
            user.save();
