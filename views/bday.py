from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from discovery.available import available_apps
from feed.models import Bit
from feed.serializers.bit import BitSerializer
from feed.serializers.bday import *
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404
import swapper
Person = swapper.load_model('kernel', 'Person')
bio_info = swapper.load_model('kernel', 'BiologicalInformation')
residential_info = swapper.load_model('kernel', 'ResidentialInformation')
from shell.models.roles.student import Student
from core.kernel.models.personal_information.base import AbstractPersonalInformation
import datetime
from django.db.models import Q
from django.views.decorators.cache import cache_page
from rest_framework.generics import GenericAPIView

class whoAmI(
    GenericAPIView
):
    """
    This view shows some personal information of the currently logged in user
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """
        person = request.person
        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

# cache_page(60 * 60 * 6)
class bdayTodayViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset for users information related to birthdate
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = PeopleSerializer
    queryset = bio_info.objects.filter(date_of_birth__month = datetime.date.today().month,date_of_birth__day= datetime.date.today().day)

    def list(self, request):
        student_ids = Student.objects.values_list('person', flat=True)
        queryset = bio_info.objects.filter(date_of_birth__month = datetime.date.today().month,date_of_birth__day= datetime.date.today().day).filter(id__in= student_ids)
        serializer = PeopleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        student_ids = Student.objects.values_list('person', flat=True)
        queryset = bio_info.objects.filter(date_of_birth__month = datetime.date.today().month,date_of_birth__day= datetime.date.today().day).filter(id__in= student_ids)
        user = get_object_or_404(queryset, pk=pk)
        serializer = PeopleSerializer(user)
        return Response(serializer.data)


# @cache_page(60 * 60 *6)
class bdayTomViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset for users information related to birthdate
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = PeopleSerializer
    queryset = bio_info.objects.filter(date_of_birth__month = datetime.date.today().month,date_of_birth__day= datetime.date.today().day)
    
    def list(self, request):
        month = (datetime.date.today() + datetime.timedelta(days=1)).month
        day = (datetime.date.today() + datetime.timedelta(days=1)).day
        student_ids = Student.objects.values_list('person', flat=True)
        queryset = bio_info.objects.filter(date_of_birth__month = month,date_of_birth__day= day).filter(id__in= student_ids)
        serializer = PeopleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        month = (datetime.date.today() + datetime.timedelta(days=1)).month
        day = (datetime.date.today() + datetime.timedelta(days=1)).day
        student_ids = Student.objects.values_list('person', flat=True)
        queryset = bio_info.objects.filter(date_of_birth__month = month,date_of_birth__day= day).filter(id__in= student_ids)
        user = get_object_or_404(queryset, pk=pk)
        serializer = PeopleSerializer(user)
        return Response(serializer.data)

# @cache_page(60 * 60*6)
class bdayDaTViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset for users information related to birthdate
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = PeopleSerializer
    queryset = bio_info.objects.filter(date_of_birth__month = datetime.date.today().month,date_of_birth__day= datetime.date.today().day)
    
    def list(self, request):
        month = (datetime.date.today() + datetime.timedelta(days=2)).month
        day = (datetime.date.today() + datetime.timedelta(days=2)).day
        student_ids = Student.objects.values_list('person', flat=True)
        queryset = bio_info.objects.filter(date_of_birth__month = month,date_of_birth__day= day).filter(id__in= student_ids)
        serializer = PeopleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        month = (datetime.date.today() + datetime.timedelta(days=2)).month
        day = (datetime.date.today() + datetime.timedelta(days=2)).day
        student_ids = Student.objects.values_list('person', flat=True)
        queryset = bio_info.objects.filter(date_of_birth__month = month,date_of_birth__day= day).filter(id__in= student_ids)
        user = get_object_or_404(queryset, pk=pk)
        serializer = PeopleSerializer(user)
        return Response(serializer.data)
