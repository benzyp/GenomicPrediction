from app.models import Patient, Embryo
from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import datetime

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
	    view_name='user-detail',
	    lookup_field='username'
    )

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
        
#class PatientSerializer(serializers.ModelSerializer):
#    #user = serializers.HyperlinkedIdentityField(
#	   # view_name='user-detail',
#	   # lookup_field='id'
#    #)
  
#    class Meta: 
#        model = Patient
#        fields = ('first_name','last_name','email','phone','user')

class PatientSerializer(serializers.ModelSerializer):
    #user = UserSerializer()# usting this will include the full user object data in the patient - not what we want
    #this code below will return the user id and it's essentially the same as the version above that uses a ModelSerializer
    #in both cases the user value is an id. removing the .lookup_field='username' yields the following error which I could not
    #get past: Could not resolve URL for hyperlinked relationship using view name "user-detail". You may have failed to include 
    #the related model in your API, or incorrectly configured the `lookup_field` attribute on this field.

    user = serializers.HyperlinkedIdentityField(
	    view_name='user-detail',
	    lookup_field='user'
    ).lookup_field='username'
  
    class Meta: 
        model = Patient
        fields = ('first_name','last_name','email','phone','user')

#using the HyperlinkedModelSerializer requires the use of the url to reference the patient on POST/Create as so:http://localhost:8000/patient/1/
#instead of using the user id
#class EmbryoSerializer(serializers.HyperlinkedModelSerializer): #using this HyperlinkModelSelector returns the patient as url to locate the data
class EmbryoSerializer(serializers.ModelSerializer): #using the ModelSerializer returns the object's id instead of a hyperlink
    class Meta:
        model = Embryo
        fields = ('code_name','karyotype','patient')

