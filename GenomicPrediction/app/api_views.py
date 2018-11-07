"""
Definition of views.
"""
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Patient, Embryo
from django.contrib.auth.models import User
from rest_framework import viewsets
from app.serializers import PatientSerializer, EmbryoSerializer, UserSerializer

#security
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework import status

from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string

from rq import Queue
from redis import Redis

import django_rq

#This mixin will save the data prior to delsting it so that it can be returned upon delete
class DestroyWithPayloadMixin(object):
     def destroy(self, *args, **kwargs):
         serializer = self.get_serializer(self.get_object())
         super().destroy(*args, **kwargs)
         return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

#Out of the box DRF viewset functionality
#class PatientViewSet(DestroyWithPayloadMixin, viewsets.ModelViewSet, APIView):
#    """
#    API endpoint that allows patient CRUD operations.
#    """
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)

#    queryset = Patient.objects.all().order_by('-created_at')
#    serializer_class = PatientSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def patient_list(request):
    """
    List all patients, or create a patient.
    """
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def patient_detail(request, pk):
    """
    Retrieve, update or delete a patient.
    """
    try:
        patient = Patient.objects.get(pk=pk)
    
    except Patient.DoesNotExist:
        return Response({'response':'Patient not found.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        #obtain object for display after delete
        serializer = PatientSerializer(patient)
        patient.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmbryoViewSet(DestroyWithPayloadMixin, viewsets.ModelViewSet, APIView):
    """
    API endpoint that allows embryo CRUD operations.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Embryo.objects.all()
    serializer_class = EmbryoSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def mail_report(request,pk):
    """Sends and email formatted as html with the patient information and embryo data
       @pk is the id of the patient
    """ 
    patient = Patient.objects.get(pk=pk)
    embryos = Embryo.objects.filter(patient=patient).all()
    for embryo in embryos:
        embryo.sex = 'M'

    data = dict({'embryos':embryos,'patient':patient})
    html_content = render_to_string('app/email.html', data)
    try:
        # Tell RQ what Redis connection to use
        #redis_conn = Redis('redis','6379')
        #q = Queue('low', connection=redis_conn)
        #q.enqueue_call(func=queue_email,args=('benzyp@yahoo.com',patient.email,html_content),)
        queue = django_rq.get_queue('low')
        queue.enqueue(queue_email, 'benzyp@yahoo.com', [patient.email], html_content)
        return Response({'response':'email sent'}, status=status.HTTP_201_CREATED)
    except Exception as e:	
        ex = e
        return Response({'response':'message failed to send.' + str(ex)}, status=status.HTTP_400_BAD_REQUEST)

def queue_email(from_email,to_email,body):
    send_mail('Your embryo report from Genomic Prediction',
        body,#TO DO - replace with plain text results - this is currently using the html formatted content
        from_email,
        to_email,
        fail_silently=False,
        html_message=body)
