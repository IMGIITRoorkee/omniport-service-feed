import swapper
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from discovery.available import available_apps
from feed.models import Bit
from feed.serializers.bit import BitSerializer
from feed.serializers.bday import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from shell.models.roles.student import Student
from core.kernel.models.personal_information.base import AbstractPersonalInformation
import datetime
from django.db.models import Q
from django.views.decorators.cache import cache_page
from rest_framework.generics import GenericAPIView
from django.core.cache import cache
Person = swapper.load_model('kernel', 'Person')
bio_info = swapper.load_model('kernel', 'BiologicalInformation')
residential_info = swapper.load_model('kernel', 'ResidentialInformation')

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
        bdaySet = cache.get('my_list_today')
        date = cache.get('date')
        if not bdaySet or date != datetime.date.today():
            student_ids = Student.objects.values_list('person', flat=True)
            bdaySet = bio_info.objects.filter(date_of_birth__month = datetime.date.today().month,date_of_birth__day= datetime.date.today().day).filter(id__in= student_ids)
            cache.set('my_list_today',bdaySet, timeout=60*60*12)
            cache.set('date',datetime.date.today(), timeout=60*60*12)
        serializer = PeopleSerializer(bdaySet, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        bdaySet = cache.get('my_list_today')
        date = cache.get('date')
        if not bdaySet or date != datetime.date.today():
            student_ids = Student.objects.values_list('person', flat=True)
            bdaySet = bio_info.objects.filter(date_of_birth__month = datetime.date.today().month,date_of_birth__day= datetime.date.today().day).filter(id__in= student_ids)
            user = get_object_or_404(bdaySet, pk=pk)
            serializer = PeopleSerializer(user)
            cache.set('my_list_today',bdaySet, timeout=60*60*12)
            cache.set('date',datetime.date.today(), timeout=60*60*12)
        serializer = PeopleSerializer(bdaySet, many=True)
        return Response(serializer.data)


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
        bdaySet = cache.get('my_list_tom')
        date = cache.get('date-tom')
        if not bdaySet or date != datetime.date.today():
            month = (datetime.date.today() + datetime.timedelta(days=1)).month
            day = (datetime.date.today() + datetime.timedelta(days=1)).day
            student_ids = Student.objects.values_list('person', flat=True)
            bdaySet = bio_info.objects.filter(date_of_birth__month = month,date_of_birth__day= day).filter(id__in= student_ids)
            cache.set('my_list_tom',bdaySet, timeout=60*60*12)
            cache.set('date-tom',datetime.date.today(), timeout=60*60*12)
        serializer = PeopleSerializer(bdaySet, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        bdaySet = cache.get('my_list_tom')
        date = cache.get('date-tom')
        if not bdaySet or date != datetime.date.today():
            month = (datetime.date.today() + datetime.timedelta(days=1)).month
            day = (datetime.date.today() + datetime.timedelta(days=1)).day
            student_ids = Student.objects.values_list('person', flat=True)
            bdaySet = bio_info.objects.filter(date_of_birth__month = month,date_of_birth__day= day).filter(id__in= student_ids)
            cache.set('my_list_tom',bdaySet, timeout=60*60*12)
            cache.set('date-tom',datetime.date.today(), timeout=60*60*12)
        serializer = PeopleSerializer(bdaySet, many=True)
        return Response(serializer.data)


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
        bdaySet = cache.get('my_list_dat')
        date = cache.get('date-dat')
        if not bdaySet or date != datetime.date.today():
            month = (datetime.date.today() + datetime.timedelta(days=2)).month
            day = (datetime.date.today() + datetime.timedelta(days=2)).day
            student_ids = Student.objects.values_list('person', flat=True)
            bdaySet = bio_info.objects.filter(date_of_birth__month = month,date_of_birth__day= day).filter(id__in= student_ids)
            cache.set('my_list_dat',bdaySet, timeout=60*60*12)
            cache.set('date-dat',datetime.date.today(), timeout=60*60*12)
        serializer = PeopleSerializer(bdaySet, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        bdaySet = cache.get('my_list_dat')
        date = cache.get('date-dat')
        if not bdaySet or date != datetime.date.today():
            month = (datetime.date.today() + datetime.timedelta(days=2)).month
            day = (datetime.date.today() + datetime.timedelta(days=2)).day
            student_ids = Student.objects.values_list('person', flat=True)
            bdaySet = bio_info.objects.filter(date_of_birth__month = month,date_of_birth__day= day).filter(id__in= student_ids)
            cache.set('my_list_dat',bdaySet, timeout=60*60*12)
            cache.set('date-dat',datetime.date.today(), timeout=60*60*12)
        serializer = PeopleSerializer(bdaySet, many=True)
        return Response(serializer.data)
