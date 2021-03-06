from django.core import serializers
from django.views import generic
from django.http import HttpResponse, QueryDict
from django.utils.http import urlquote
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from birthdaycal.auth_data import CLIENT #client data
from models import Doctor, Patient
from forms import EmailForm, PatientForm
from helper import get_drchrono_user

# Create your views here.


def login_view(request):
    return render(request, 'generic/login.html',
                  context={'redirect_url': urlquote(CLIENT['redirect_url']),
                            'client_id': CLIENT['client_id']})


def oauth_view(request):
    """
    Redirect here. Handles user login and updating db with new drchrono data.
    """
    if 'error' in request.GET:
        return redirect('birthcal:login_error')

    user = get_drchrono_user(request.GET)
    auth_user = authenticate(
        username=user.username,
        password=user.doctor.set_random_password()
    )
    login(request, auth_user)
    return redirect('birthcal:index_view')


def login_error_view(request):
    """
    If drchrono authentication fails
    """
    return render(request, 'generic/error.html')


def logout_view(request):
    logout(request)
    return redirect('birthcal:index_view')


def index_view(request):
    """
    Landing page
    """
    doctor = request.user.doctor
    patients = doctor.patient_set.all()
    context = {
        'doctor': doctor,
        'patients': patients,
        'username': request.user.username,
        'redirect_url': urlquote(CLIENT['redirect_url']),
        'client_id': CLIENT['client_id'],
        'is_guest': request.user.username == 'guest'
    }

    return render(request, 'index.html', context)


def edit_email_view(request):
    user = request.user
    doctor = user.doctor
    context = {
        'user': user,
        'email_subject': doctor.email_subject.format(doctor.last_name),
        'email_body': doctor.email_body.format(doctor.last_name),
    }

    return render(request, 'email.html', context)


class DoctorView(generic.DetailView):
    model = Doctor

    def patch(self, request, **kwargs):
        doctor = get_object_or_404(User, pk=kwargs['pk']).doctor
        data = QueryDict(request.body)
        form = EmailForm(data, instance=doctor)
        if form.is_valid():
            form.save()
            doctorJSON = serializers.serialize("json", [doctor])
            return HttpResponse(doctorJSON, content_type='application/json')

        return HttpResponse(status=500)


class PatientView(generic.DetailView):
    model = Patient

    def patch(self, request, **kwargs):
        patient = get_object_or_404(Patient, pk=kwargs['pk'])
        data = QueryDict(request.body)
        form = PatientForm(data, instance=patient)
        if form.is_valid():
            form.save()
            patientJSON = serializers.serialize("json", [patient])
            return HttpResponse(patientJSON, content_type='application/json')

        return HttpResponse(status=500)