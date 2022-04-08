import swapper
from rest_framework import serializers
from omniport.utils import switcher

Person = swapper.load_model('kernel', 'Person')
BiologicalInformation = swapper.load_model('kernel', 'BiologicalInformation')
StudentSerializer = switcher.load_serializer('kernel', 'Student')


class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer for Person objects
    """
    residentialinformation = serializers.SerializerMethodField()
    student = StudentSerializer(
        excluded_fields=['person', 'enrolment_number', 'current_semester'])
    membership_set = serializers.SerializerMethodField()

    def get_residentialinformation(self, instance):
        try:
            residentialinformation = instance.residentialinformation
            return residentialinformation.residence.code
        except:
            return None

    def get_membership_set(self, instance):
        try:
            membership_set = instance.membership_set.all()
            group = [membership.group.id for membership in membership_set]
            return group
        except:
            return []

    class Meta:
        model = Person
        read_only_fields = ['student']
        exclude = ('local_guardians', 'spouses', 'parents',)


class BiologicalInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for Biological information with necessary residential and student information
    """
    person = PersonSerializer()

    class Meta:
        model = BiologicalInformation
        fields = ['id', 'person']
