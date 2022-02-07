import swapper
from rest_framework import serializers
from omniport.utils import switcher
from shell.models.institute.residence import Residence
from shell.models.roles.student import Student
from groups.models.membership import Membership
AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')
Person = swapper.load_model('kernel', 'Person')
bio_info = swapper.load_model('kernel', 'BiologicalInformation')
residential_info = swapper.load_model('kernel', 'ResidentialInformation')
branch = swapper.load_model('kernel', 'Branch')
BranchSerializer = switcher.load_serializer('kernel', 'Branch')
ResidenceSerializer = switcher.load_serializer('kernel', 'Residence')


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student objects
    """
    branch = BranchSerializer()

    class Meta:
        model = Student
        fields = ['id', 'current_year', 'current_semester',
                  'enrolment_number', 'branch']


class ResidentialinfoSerializer(serializers.ModelSerializer):
    """
    Serializer for Residence information of people
    """
    residence = ResidenceSerializer()

    class Meta:
        model = residential_info
        fields = ['id', 'residence', 'person']


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
    student = StudentSerializer()
    membership_set = MembershipSerializer(many=True)

    class Meta:
        model = Person
        fields = '__all__'


class PeopleSerializer(serializers.ModelSerializer):
    """
    Serializer for Person objects
    """
    person = PersonSerializer()

    class Meta:
        model = bio_info
        fields = ['id', 'person', 'date_of_birth', 'gender']
