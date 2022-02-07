from django import urls
import swapper
import datetime
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from feed.serializers.bday import PersonSerializer, PeopleSerializer
from shell.models.roles.student import Student
from core.kernel.models.personal_information.base import AbstractPersonalInformation

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


class bdayViewSet(
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

    def get_queryset(self):
        student_ids = Student.objects.values_list('person', flat=True)
        if(self.request.query_params.get('bdayDay') == "today"):
            queryset = cache.get('my_list_today')
            date = cache.get('date')
            if not queryset or date != datetime.date.today():
                queryset = bio_info.objects.filter(date_of_birth__month=datetime.date.today(
                ).month, date_of_birth__day=datetime.date.today().day).filter(id__in=student_ids)
                cache.set('my_list_today', queryset, timeout=60*60*12)
                cache.set('date', datetime.date.today(), timeout=60*60*12)

        if(self.request.query_params.get('bdayDay') == "tom"):
            queryset = cache.get('my_list_tom')
            date = cache.get('date-tom')
            if not queryset or date != datetime.date.today():
                month = (datetime.date.today() +
                         datetime.timedelta(days=1)).month
                day = (datetime.date.today() + datetime.timedelta(days=1)).day
                queryset = bio_info.objects.filter(
                    date_of_birth__month=month, date_of_birth__day=day).filter(id__in=student_ids)
                cache.set('my_list_tom', queryset, timeout=60*60*12)
                cache.set('date-tom', datetime.date.today(), timeout=60*60*12)

        if(self.request.query_params.get('bdayDay') == "dat"):
            queryset = cache.get('my_list_dat')
            date = cache.get('date-dat')
            if not queryset or date != datetime.date.today():
                month = (datetime.date.today() +
                         datetime.timedelta(days=2)).month
                day = (datetime.date.today() + datetime.timedelta(days=2)).day
                queryset = bio_info.objects.filter(
                    date_of_birth__month=month, date_of_birth__day=day).filter(id__in=student_ids)
                cache.set('my_list_dat', queryset, timeout=60*60*12)
                cache.set('date-dat', datetime.date.today(), timeout=60*60*12)
        return queryset
