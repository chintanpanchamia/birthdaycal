__author__ = 'chintanpanchamia'

from django.core.management.base import BaseCommand
from birthcal.models import Doctor
from django.core.mail import send_mass_mail

import datetime

from birthdaycal.auth_data import EMAIL_HOST_USER


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        def is_today_birthday(patient):
            currentDate = datetime.date.today()
            birthday = patient.dob
            if (birthday.month == currentDate.month and
                    birthday.day == currentDate.day):
                return True

            return False

        def email(doctor, patient):

            body = doctor.email_body.format(doctor.last_name)
            body = body.replace(
                '[fn]', patient.first_name
            ).replace(
                '[ln]', patient.last_name
            )

            message = (doctor.email_subject, body, EMAIL_HOST_USER, [patient.email])
            return message

        def get_bday_emails(doctor):
            emails = []
            patients = doctor.patient_set.filter(send_email=True)
            for patient in patients:
                if is_today_birthday(patient):
                    message = (email(doctor, patient))
                    emails.append(message)

            return emails




        doctors = Doctor.objects.all()
        emails = []
        for doctor in doctors:
            emails.extend(get_bday_emails(doctor))

        send_mass_mail(tuple(emails), fail_silently=False)