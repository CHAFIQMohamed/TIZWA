from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from accreditation.models import Accreditation
from accreditation.models import Syllabus
from accreditation.models import Intervention


# =======================================================
class CreateAccreditationForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['kind', 'name', 'title', 'institute', 
                  'specialty1', 'specialty2', 'specialty3', 'specialty4']

    def save(self, commit=True):
        accreditation = self.instance

        accreditation.kind = self.cleaned_data['kind']
        accreditation.name = self.cleaned_data['name']
        accreditation.title = self.cleaned_data['title']
        accreditation.institute = self.cleaned_data['institute']

        accreditation.specialty2 = self.cleaned_data['specialty2']
        accreditation.specialty3 = self.cleaned_data['specialty3']
        accreditation.specialty4 = self.cleaned_data['specialty4']

        specialty1 = self.cleaned_data['specialty1']
        if not specialty1:
            specialty1 = accreditation.title
        accreditation.specialty1 = specialty1
        
        if commit:
            accreditation.save()

        return accreditation       

# =======================================================
class CreateSyllabusForm(forms.ModelForm):

    class Meta:
        model = Syllabus
        fields = ['name', 'title', 'goals', 'description', 
        'evaluation', 'grad', 'validation']


# =======================================================
class UpdateAccreditationForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['goals',  'areas', 'acquired_skills', 'careers']

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.goals = self.cleaned_data['goals']
        accreditation.areas = self.cleaned_data['areas']
        accreditation.acquired_skills = self.cleaned_data['acquired_skills']
        accreditation.careers = self.cleaned_data['careers']
        
        if commit:
            accreditation.save()

        return accreditation  

# =======================================================
class AccreditationGeneralForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['options', 'keywords', 'domains'] 

    def save(self, commit=True):
        accreditation = self.instance

        accreditation.options = self.cleaned_data['options']
        accreditation.keywords = self.cleaned_data['keywords']
        accreditation.domains = self.cleaned_data['domains']
        
        if commit:
            accreditation.save()

        return accreditation            

# =======================================================
class AccreditationGoalsForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['goals',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.goals = self.cleaned_data['goals']
        
        if commit:
            accreditation.save()

        return accreditation        

# =======================================================
class AccreditationAreasForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['areas',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.areas = self.cleaned_data['areas']
        
        if commit:
            accreditation.save()

        return accreditation     

# =======================================================
class AccreditationAcquiredSkillsForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['acquired_skills',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.acquired_skills = self.cleaned_data['acquired_skills']
        
        if commit:
            accreditation.save()

        return accreditation       

# =======================================================
class AccreditationCareersForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['careers',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.careers = self.cleaned_data['careers']
        
        if commit:
            accreditation.save()

        return accreditation     

# =======================================================
class AccreditationAccessDiplomaForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['access_diploma',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.access_diploma = self.cleaned_data['access_diploma']
        
        if commit:
            accreditation.save()

        return accreditation           

# =======================================================
class AccreditationAccessPrerequisiteForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['access_prerequisite',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.access_prerequisite = self.cleaned_data['access_prerequisite']
        
        if commit:
            accreditation.save()

        return accreditation   

# =======================================================
class AccreditationAccessSelectionForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['access_selection',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.access_selection = self.cleaned_data['access_selection']
        
        if commit:
            accreditation.save()

        return accreditation   

# =======================================================
class AccreditationAccessFileForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['access_file',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.access_file = self.cleaned_data['access_file']
        
        if commit:
            accreditation.save()

        return accreditation   

# =======================================================
class AccreditationAccessExamForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['access_exam',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.access_exam = self.cleaned_data['access_exam']
        
        if commit:
            accreditation.save()

        return accreditation                                   

# =======================================================
class AccreditationAccessInterviewForm(forms.ModelForm):

    class Meta:
        model = Accreditation
        fields = ['access_interview',] 

    def save(self, commit=True):
        accreditation = self.instance
                
        accreditation.access_interview = self.cleaned_data['access_interview']
        
        if commit:
            accreditation.save()

        return accreditation 

# =======================================================
class SyllabusGoalsForm(forms.ModelForm):

    class Meta:
        model = Syllabus
        fields = ['goals',] 

    def save(self, commit=True):
        syllabus = self.instance
                
        syllabus.goals = self.cleaned_data['goals']
        
        if commit:
            syllabus.save()

        return syllabus    

# =======================================================
class SyllabusDescriptionForm(forms.ModelForm):

    class Meta:
        model = Syllabus
        fields = ['description',] 

    def save(self, commit=True):
        syllabus = self.instance
                
        syllabus.description = self.cleaned_data['description']
        
        if commit:
            syllabus.save()

        return syllabus   

# =======================================================
class SyllabusEvaluationForm(forms.ModelForm):

    class Meta:
        model = Syllabus
        fields = ['evaluation',] 

    def save(self, commit=True):
        syllabus = self.instance
                
        syllabus.evaluation = self.cleaned_data['evaluation']
        
        if commit:
            syllabus.save()

        return syllabus   

# =======================================================
class SyllabusGradForm(forms.ModelForm):

    class Meta:
        model = Syllabus
        fields = ['grad',] 

    def save(self, commit=True):
        syllabus = self.instance
                
        syllabus.grad = self.cleaned_data['grad']
        
        if commit:
            syllabus.save()

        return syllabus   

# =======================================================
class SyllabusValidationForm(forms.ModelForm):

    class Meta:
        model = Syllabus
        fields = ['validation',] 

    def save(self, commit=True):
        syllabus = self.instance
                
        syllabus.validation = self.cleaned_data['validation']
        
        if commit:
            syllabus.save()

        return syllabus     

# =======================================================
class SyllabusGeneralForm(forms.ModelForm):

    class Meta:
        model = Syllabus
        fields = ['title', 'subelement1', 'subelement2'] 

    def save(self, commit=True):
        syllabus = self.instance
        title = self.cleaned_data['title']

        syllabus.title = title
        syllabus.subelement2 = self.cleaned_data['subelement2']

        subelement1 = self.cleaned_data['subelement1']
        if not subelement1:
            subelement1 = title
        syllabus.subelement1 = subelement1
        
        if commit:
            syllabus.save()

        return syllabus      

# =======================================================
class CreateSyllabusInteventionForm(forms.ModelForm):

    class Meta:
        model = Intervention
        fields = ['kind', 'component', 'duration']              