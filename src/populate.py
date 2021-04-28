import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tizwa.settings') #koka

import django
django.setup()

from django.shortcuts import get_object_or_404

import pandas as pd
from pandas import read_excel

from account.models import Account

# =======================================================
def createsuperuser():
    email = "admin@tizwa.ma"
    username = "admin"
    last_name = "admin"
    first_name = "admin"
    password = 'TIZWA@LSD'

    admin = Account.objects.create_superuser(email, username, last_name, first_name, password=password)
    admin.save()

# =======================================================
def populate_professors():
    # read excel file
    filename = '../data/professors.xlsx'
    if not os.path.isfile(filename):
        raise ValueError('Could not find the filename {}'.format(filename))

    df = read_excel(filename)

    all_email = df['email']
    all_last_name = df['last_name']
    all_first_name = df['first_name']
    all_profile = df['profile']
    all_grad = df['grad']
    all_expertize = df['expertize']
    all_university = df['university']
    all_departement = df['departement']
    all_tel = df['tel']

    all_data = zip(all_email, all_last_name, all_first_name, all_profile,
                   all_grad, all_expertize, all_university, all_departement, all_tel)

    for (email, last_name, first_name, profile,
         grad, expertize, university, departement, tel) in all_data:

        # TODO improve
        username = email.split('@')[0]
        password = 'TIZWA@LSD'

        professor = Account.objects.create_user(email, username, last_name, first_name, password=password)
        professor.profile = profile
        professor.grad = grad
        professor.expertize = expertize
        professor.university = university
        professor.departement = departement
        professor.tel = tel
        professor.is_professor = True
        professor.save()

#############################################################
if __name__ == '__main__':
    print("Starting population script...")

    createsuperuser()
    populate_professors()
