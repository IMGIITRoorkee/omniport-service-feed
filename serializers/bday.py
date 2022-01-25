from rest_framework import serializers

from configuration.serializers.app.app import AppSerializer
from feed.models import Bit
from omniport.utils import switcher

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')
import swapper
Person = swapper.load_model('kernel', 'Person')
bio_info = swapper.load_model('kernel', 'BiologicalInformation')
residential_info = swapper.load_model('kernel', 'ResidentialInformation')
branch = swapper.load_model('kernel', 'Branch')
from shell.models.institute.residence import Residence
from shell.models.roles.student import Student
from groups.models.membership import Membership

class BranchSerializer(serializers.ModelSerializer):
    """
    Serializer for Branches in institute
    """
    class Meta:
        model = branch
        fields = ['id','code','name']

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student objects
    """
    branch = BranchSerializer()
    class Meta:
        model = Student
        fields = ['id', 'person', 'current_year','current_semester','enrolment_number','branch']

class ResidenceSerializer(serializers.ModelSerializer):
    """
    Serializer for Residence 
    """
    class Meta:
        model = Residence
        fields = ['id','code']

class ResidentialinfoSerializer(serializers.ModelSerializer):
    """
    Serializer for Residence information of people
    """
    residence = ResidenceSerializer()
    # person = PersonSerializer()
    class Meta:
        model = residential_info
        fields = ['id', 'residence','person']

class MembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for Membership of groups
    """
    class Meta:
        model = Membership
        fields = ['group']

class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer for Person objects
    """
    residentialinformation = ResidentialinfoSerializer()
    student =  StudentSerializer()
    membership_set = MembershipSerializer(many= True)
    class Meta:
        model = Person
        fields = '__all__'



class PeopleSerializer(serializers.ModelSerializer):
    """
    Serializer for Person objects
    """
    person = PersonSerializer()
    # res = ResidentialSerializer()
    class Meta:
        model = bio_info
        fields = ['id','person','date_of_birth','gender']
