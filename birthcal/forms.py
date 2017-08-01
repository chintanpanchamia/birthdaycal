__author__ = 'chintanpanchamia'

from django import forms

from models import Doctor, Patient


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['send_email']


class EmailForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['email_subject', 'email_body']
