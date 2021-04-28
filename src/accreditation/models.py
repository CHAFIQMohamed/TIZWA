import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings

#from ckeditor.fields import RichTextField as TextField
from mdeditor.fields import MDTextField as TextField

# =======================================================
class Accreditation(models.Model):

    # TODO rajouter le champ <th>options</th>

    kind = models.CharField(max_length=15, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    institute = models.CharField(max_length=50, null=False, blank=False)
    options = models.CharField(max_length=50, blank=True, null=True)
    keywords = models.CharField(max_length=300, blank=True, null=True) # TODO change field type
    domains = models.CharField(max_length=300, blank=True, null=True) # TODO change field type
    specialty1 = models.CharField(max_length=50, blank=True, null=True)
    specialty2 = models.CharField(max_length=50, blank=True, null=True)
    specialty3 = models.CharField(max_length=50, blank=True, null=True)
    specialty4 = models.CharField(max_length=50, blank=True, null=True)
    goals = TextField(blank=True, null=True)
    areas = TextField(blank=True, null=True)
    acquired_skills = TextField(blank=True, null=True)
    careers = TextField(blank=True, null=True)
    # TODO should we put this in a table with a one-to-one relation with accreditation?
    access_diploma = TextField(blank=True, null=True)
    access_prerequisite = TextField(blank=True, null=True)
    access_selection = TextField(blank=True, null=True)
    access_file = TextField(blank=True, null=True)
    access_exam = TextField(blank=True, null=True)
    access_interview = TextField(blank=True, null=True)
    #articulation = TextField(blank=True, null=True)
    approval_number = models.CharField(max_length=15)

    is_ongoing = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    date_approved = models.DateTimeField(auto_now_add=True, verbose_name="approval date ")
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="creation date")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")

    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def approve(self):
        self.is_approved.set(True)
        self.is_ongoing.set(False)

    def activate(self):
        self.is_active.set(True)
    
    @property
    def n_specialties(self):
        n = 1
        if self.specialty2:
            n +=1 
        if self.specialty3:
            n +=1         
        if self.specialty4:
            n +=1         
        return n    

    @property
    def n_semesters(self):
        if self.kind.lower() == "master":
            return 4

        else:
            raise ValueError('{} not available yet'.format(self.kind))

# =======================================================
class Syllabus(models.Model):

    accreditation = models.ForeignKey(Accreditation, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    goals = TextField(blank=True, null=True)
    description = TextField(blank=True, null=True)
    subelement1 = models.CharField(max_length=50, blank=True, null=True)
    subelement2 = models.CharField(max_length=50, blank=True, null=True)
    semester = models.IntegerField() # TODO use choice?

    status = models.CharField(max_length=50, blank=True, null=True) # TODO use choice?

    # ... evaluation
    # Modes D’évaluation
    evaluation = TextField(blank=True, null=True)
    # Note Du Module
    grad = TextField(blank=True, null=True)
    # Modalités De Validation Du Module
    validation = TextField(blank=True, null=True)
    # ...

    # Autres Eléments Pertinents   TODO to be computed
    is_approved = models.BooleanField(default=False)

    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")

    def __str__(self):
        return self.name    

    def is_valid_attribut(self, key):
        # TODO remove
        if key == 'evaluation':
            return not(str(self.evaluation) == '')

        if key == 'grad':
            return not(str(self.grad) == '')

        if key == 'validation':
            return not(str(self.validation) == '')

        return False

    def get_pedagogical_team(self):
        # TODO remove
        raise NotImplementedError('TODO')

# =======================================================
class Intervention(models.Model):

    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    component = models.CharField(max_length=50)
    kind = models.CharField(max_length=10)
    duration = models.IntegerField()

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.syllabus) + '_' + str(self.professor.last_name) + '_' + str(self.professor.first_name)

        