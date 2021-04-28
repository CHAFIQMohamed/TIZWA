from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from itertools import groupby

from notifications.signals import notify
from markdown import markdown



from accreditation.models import Accreditation
from accreditation.models import Syllabus
from accreditation.models import Intervention
from accreditation.forms import CreateAccreditationForm, UpdateAccreditationForm
from accreditation.forms import CreateSyllabusForm
from accreditation.forms import AccreditationGoalsForm, AccreditationGeneralForm
from accreditation.forms import AccreditationAreasForm
from accreditation.forms import AccreditationAcquiredSkillsForm
from accreditation.forms import AccreditationCareersForm
from accreditation.forms import SyllabusGoalsForm
from accreditation.forms import SyllabusDescriptionForm
from accreditation.forms import SyllabusEvaluationForm
from accreditation.forms import SyllabusGradForm
from accreditation.forms import SyllabusValidationForm
from accreditation.forms import SyllabusGeneralForm
from accreditation.forms import CreateSyllabusInteventionForm

from accreditation.forms import ( AccreditationAccessDiplomaForm,
                                  AccreditationAccessExamForm,
                                  AccreditationAccessFileForm,
                                  AccreditationAccessInterviewForm,
                                  AccreditationAccessPrerequisiteForm,
                                  AccreditationAccessSelectionForm,
                                  )


from accreditation.codegen import model_to_md

from account.models import Account


# =======================================================
def accreditation_view(request):

    context = {}

    return render(request, 'accreditation/home.html', context)

# =======================================================
def create_accreditation_view(request):
    """
    by default, the coordinator of a syllabus is initialized to the accreditation coordinator.
    Account is a ForeignKey and the coordinator must be given when creating the Syllabus.
    """
    context = {}

    # ...
    modules = Syllabus.objects.all()

    context['modules'] = modules
    for module in modules:
        print(module.title)
    # ...

    # ... TODO improve.
    #          add list of professors or program lead?
    #          sort by last name
    accounts = Account.objects.filter(is_professor=True)
    context['accounts'] = accounts
    # ...

    form = CreateAccreditationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)

        email = request.POST['coordinator'] # TODO use cleand_data
        coordinator = Account.objects.filter(email=email).first()
        obj.coordinator = coordinator

        obj.save()
        form = CreateAccreditationForm()

        # ...
        accreditation = Accreditation.objects.filter(name=request.POST['name']).first()
        n_specialties = accreditation.n_specialties
        if accreditation.kind.lower() == "master":
            n_common = 12
            if n_specialties == 1:
                n_common += 6

            # common modules
            for i in range(0, n_common):
                label = 'M{}'.format(i+1)
                semester = ( i // 6 ) + 1 # 6 modules per semester. TODO Bachelor case
                module = Syllabus(accreditation=accreditation,
                                  name=label,
                                  semester=semester,
                                  coordinator=accreditation.coordinator,
                                  status='ongoing')
                module.save()

            # specialities
            if n_specialties > 1:
                for i in range(n_common, n_common+6):
                    _label = 'M{}'.format(i+1)
                    semester = 3

                    for s,tag in zip(range(n_specialties), ['a', 'b', 'c', 'd']): # TODO improve
                        label = '{label}{tag}'.format(label=_label, tag=tag)
                        module = Syllabus(accreditation=accreditation,
                                          name=label,
                                          semester=semester,
                                          coordinator=accreditation.coordinator,
                                          status='ongoing')
                        module.save()

        else:
            raise ValueError('{} not available yet'.format(accreditation.kind))
        # ...

        # ... send notification
        notify.send(request.user,
                    recipient=coordinator,
                    verb='you were assigned as the coordinator of an accreditation',
                    target=accreditation,
                    )
        # ...

        return redirect('dashboard:home')

    context['form'] = form

    return render(request, 'accreditation/create_accreditation.html', context)

# =======================================================
# TODO remove
def create_syllabus_view(request):
    context = {}

    form = CreateSyllabusForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = CreateSyllabusForm()

    context['form'] = form

    return render(request, 'accreditation/create_syllabus.html', context)

# =======================================================
def edit_accreditation_view(request, name):
    context = {}

    # ...
    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation
    # ...

    # ...
    syllabuses = Syllabus.objects.filter(accreditation=accreditation)
    context['syllabuses'] = syllabuses
    # ...

    # ... TODO improve
    context['semester1'] = syllabuses.filter(semester=1)
    context['semester2'] = syllabuses.filter(semester=2)
    context['semester3'] = syllabuses.filter(semester=3)

    if not( accreditation.kind.lower() == 'master' ):
        raise NotImplementedError('{} not treated yet'.format(accreditation.kind))
    # ...

    return render(request, 'accreditation/edit_accreditation.html', context)

# =======================================================
# TODO must use accreditation name in args
def edit_accreditation_general_view(request, name):
    context = {}

    # ... TODO improve.
    #          sort by last name
    accounts = Account.objects.filter(is_professor=True)
    context['accounts'] = accounts
    # ...

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationGeneralForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)

            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationGeneralForm(initial={"options": accreditation.options,
                                             "keywords": accreditation.keywords,
                                             "domains": accreditation.domains,
                                             }
            )

    context['form'] = form

    return render(request, 'accreditation/edit_accreditation_general.html', context)

# =======================================================
def edit_accreditation_goals_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationGoalsForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationGoalsForm(
            initial={"goals": accreditation.goals,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_areas_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationAreasForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationAreasForm(
            initial={"areas": accreditation.areas,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_acquired_skills_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationAcquiredSkillsForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationAcquiredSkillsForm(
            initial={"acquired_skills": accreditation.acquired_skills,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_careers_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationCareersForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationCareersForm(
            initial={"careers": accreditation.careers,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_access_diploma_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationAccessDiplomaForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationAccessDiplomaForm(
            initial={"access_diploma": accreditation.access_diploma,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_access_prerequisite_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationAccessPrerequisiteForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationAccessPrerequisiteForm(
            initial={"access_prerequisite": accreditation.access_prerequisite,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_access_selection_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationAccessSelectionForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationAccessSelectionForm(
            initial={"access_selection": accreditation.access_selection,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_access_file_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationAccessFileForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationAccessFileForm(
            initial={"access_file": accreditation.access_file,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_access_exam_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationAccessExamForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationAccessExamForm(
            initial={"access_exam": accreditation.access_exam,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_access_interview_view(request, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation

    if request.POST:
        form = AccreditationAccessInterviewForm(request.POST or None, request.FILES or None, instance=accreditation)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_accreditation', name=name)

    form = AccreditationAccessInterviewForm(
            initial={"access_interview": accreditation.access_interview,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
def edit_accreditation_syllabus_view(request, name):
    context = {}

    # ...
    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation
    # ...

    # ...
    syllabuses = Syllabus.objects.filter(accreditation=accreditation)
    context['syllabuses'] = syllabuses
    # ...

    # ... TODO improve
    context['semester1'] = syllabuses.filter(semester=1)
    context['semester2'] = syllabuses.filter(semester=2)
    context['semester3'] = syllabuses.filter(semester=3)

    if not( accreditation.kind.lower() == 'master' ):
        raise NotImplementedError('{} not treated yet'.format(accreditation.kind))
    # ...

    return render(request, 'accreditation/edit_accreditation_syllabus.html', context)

# =======================================================
# TODO must use accreditation name in args
def edit_syllabus_view(request, accreditation_name, name):
    context = {}

    # ...
    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    context['accreditation'] = accreditation
    # ...

    # ...
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()
    context['syllabus'] = syllabus
    # ...

    # ...
    interventions = Intervention.objects.filter(syllabus=syllabus)
    context['interventions'] = interventions
    # ...

    # ...
    _COLORS = ["#a6374b", "#f2c12e", "#2e5b2e", "#4946a6", "#542082",
               "#4d918f", "#8ec3b3", "#f7ca89", "#f7ad97", "#f5907b"] # TODO improve and make it bigger
    # ...

    # ...
    def construct_chart_kind(interventions):
        """
        construct a chart of interverntions grouped by kind
        """
        COLORS = _COLORS.copy() # TODO improve

        labels = []
        values = []
        colors = []
        keyfunc = lambda x: x.kind
        interventions = sorted(interventions, key=keyfunc)
        for kind, group in groupby(interventions, keyfunc):
            value = sum([intervention.duration for intervention in group])

            values.append(value)
            labels.append(kind)
            colors.append(COLORS.pop())

        total_expected = 50 # TODO must be defined for every kind of Accreditation
        total_effective = sum(values)
        remaining = total_expected - total_effective

        if remaining > 0:
            values.append(remaining)
            labels.append('Remaining')
            colors.append('#808080')

        return {'chart_kind_values': json.dumps(values),
                'chart_kind_labels': json.dumps(labels),
                'chart_kind_colors': json.dumps(colors)
        }
    # ...

    # ...
    def construct_chart_professor(interventions):
        """
        construct a chart of interverntions grouped by professor
        """
        COLORS = _COLORS.copy() # TODO improve

        labels = []
        values = []
        colors = []

        keyfunc = lambda x: x.professor.email
        interventions = sorted(interventions, key=keyfunc)
        for professor, group in groupby(interventions, keyfunc):
            value = sum([intervention.duration for intervention in group])
            values.append(value)
            # TODO put Professor lastname and firstname in label
            #labels.append('{fname} {lname}'.format(fname=professor.first_name,  lname=professor.last_name))
            labels.append(professor)
            colors.append(COLORS.pop())

        total_expected = 50 # TODO must be defined for every kind of Accreditation
        total_effective = sum(values)
        remaining = total_expected - total_effective

        if remaining > 0:
            values.append(remaining)
            labels.append('Remaining')
            colors.append('#808080')

        return {'chart_professor_values': json.dumps(values),
                'chart_professor_labels': json.dumps(labels),
                'chart_professor_colors': json.dumps(colors)
        }
    # ...

    # ...
    d = construct_chart_kind(interventions)
    for k,v in d.items():
        context[k] = v
    # ...

    # ...
    d = construct_chart_professor(interventions)
    for k,v in d.items():
        context[k] = v
    # ...

    return render(request, 'accreditation/edit_syllabus.html', context)

# =======================================================
# TODO must use accreditation name in args
def edit_syllabus_goals_view(request, accreditation_name, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus

    if request.POST:
        form = SyllabusGoalsForm(request.POST or None, request.FILES or None, instance=syllabus)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_syllabus', name=name, accreditation_name=accreditation_name)

    form = SyllabusGoalsForm(
            initial={"goals": syllabus.goals,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
# TODO must use accreditation name in args
def edit_syllabus_description_view(request, accreditation_name, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus

    if request.POST:
        form = SyllabusDescriptionForm(request.POST or None, request.FILES or None, instance=syllabus)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_syllabus', name=name, accreditation_name=accreditation_name)

    form = SyllabusDescriptionForm(
            initial={"description": syllabus.description,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
# TODO must use accreditation name in args
def edit_syllabus_evaluation_view(request, accreditation_name, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus

    if request.POST:
        form = SyllabusEvaluationForm(request.POST or None, request.FILES or None, instance=syllabus)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_syllabus', name=name, accreditation_name=accreditation_name)

    form = SyllabusEvaluationForm(
            initial={"evaluation": syllabus.evaluation,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
# TODO must use accreditation name in args
def edit_syllabus_grad_view(request, accreditation_name, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus

    if request.POST:
        form = SyllabusGradForm(request.POST or None, request.FILES or None, instance=syllabus)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_syllabus', name=name, accreditation_name=accreditation_name)

    form = SyllabusGradForm(
            initial={"grad": syllabus.grad,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
# TODO must use accreditation name in args
def edit_syllabus_validation_view(request, accreditation_name, name):
    context = {}

    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus

    if request.POST:
        form = SyllabusValidationForm(request.POST or None, request.FILES or None, instance=syllabus)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect('accreditation:edit_syllabus', name=name, accreditation_name=accreditation_name)

    form = SyllabusValidationForm(
            initial={"validation": syllabus.validation,}
            )
    context['form'] = form

    return render(request, 'accreditation/edit_textarea.html', context)

# =======================================================
# TODO must use accreditation name in args
def edit_syllabus_general_view(request, accreditation_name, name):
    context = {}

    # ... TODO improve.
    #          sort by last name
    accounts = Account.objects.filter(is_professor=True)
    context['accounts'] = accounts
    # ...

    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus

    if request.POST:
        form = SyllabusGeneralForm(request.POST or None, request.FILES or None, instance=syllabus)
        if form.is_valid():
            obj = form.save(commit=False)

            email = request.POST['coordinator'] # TODO use cleand_data
            coordinator = Account.objects.filter(email=email).first()
            obj.coordinator = coordinator

            obj.save()

            # ... send notification
            notify.send(request.user,
                        recipient=coordinator,
                        verb='you were assigned as the coordinator of a syllabus',
                        target=syllabus,
                        )
            # ...

            return redirect('accreditation:edit_syllabus', name=name, accreditation_name=accreditation_name)

    form = SyllabusGeneralForm(initial={"title": syllabus.title,
                                        "subelement1": syllabus.subelement1,
                                        "subelement2": syllabus.subelement2}
            )

    context['form'] = form

    return render(request, 'accreditation/edit_syllabus_general.html', context)

# =======================================================
# TODO must use accreditation name in args
def edit_syllabus_intervention_view(request, accreditation_name, name):
    context = {}

    # ...
    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus
    # ...

    # ... TODO improve.
    #          sort by last name
    accounts = Account.objects.filter(is_professor=True)
    context['accounts'] = accounts
    # ...

    form = CreateSyllabusInteventionForm(request.POST or None, request.FILES or None)

    if form.is_valid():

        obj = form.save(commit=False)

        email = request.POST['professor'] # TODO use cleand_data
        professor = Account.objects.filter(email=email).first()
        obj.professor = professor

        obj.syllabus = syllabus

        obj.save()

        # ... send notification
        notify.send(request.user,
                    recipient=professor,
                    verb='you were assigned an accreditation intervention',
                    target=syllabus,
                    )
        # ...

        return redirect('accreditation:edit_syllabus', name=name, accreditation_name=accreditation_name)

    context['form'] = form

    return render(request, 'accreditation/edit_syllabus_intervention.html', context)

# =======================================================
def detail_accreditation_view(request, name):
    context = {}

    # ...
    accreditation = get_object_or_404(Accreditation, name=name)
    context['accreditation'] = accreditation
    # ...

    # ...
    content = model_to_md(accreditation, level=1)

    context['md_data_as_html'] = markdown(content['data'])
    context['md_toc_as_html'] = markdown(content['toc'])

    # print('============= MD   =============')
    # print('>>> DATA')
    # print(content['data'])
    # print('>>> TOC')
    # print(content['toc'])
    # print('================================')
    # print('============= HTML =============')
    # print('>>> DATA')
    # print(context['md_data_as_html'])
    # print('>>> TOC')
    # print(context['md_toc_as_html'])
    # print('================================')
    # ...

    return render(request, 'accreditation/detail_accreditation.html', context)

# =======================================================
def detail_syllabus_view(request, accreditation_name, name):
    context = {}

    # ...
    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus
    # ...

    # ...
    content = model_to_md(syllabus, level=1)

    context['md_data_as_html'] = markdown(content['data'])
    context['md_toc_as_html'] = markdown(content['toc'])

    # print('============= MD   =============')
    # print('>>> DATA')
    # print(content['data'])
    # print('>>> TOC')
    # print(content['toc'])
    # print('================================')
    # print('============= HTML =============')
    # print('>>> DATA')
    # print(context['md_data_as_html'])
    # print('>>> TOC')
    # print(context['md_toc_as_html'])
    # print('================================')
    # ...

    return render(request, 'accreditation/detail_syllabus.html', context)

# =======================================================
def request_approval_syllabus_view(request, accreditation_name, name):
    context = {}

    # ...
    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus
    # ...

    # ...
    if request.POST:
        syllabus.status = 'pending'
        syllabus.save()

        return redirect('accreditation:edit_syllabus', name=name, accreditation_name=accreditation_name)
    # ...

    return render(request, 'accreditation/request_approval_syllabus.html', context)

# =======================================================
def approve_syllabus_view(request, accreditation_name, name):
    context = {}

    # ...
    accreditation = get_object_or_404(Accreditation, name=accreditation_name)
    syllabus = Syllabus.objects.filter(accreditation=accreditation).filter(name=name).first()

    context['accreditation'] = accreditation
    context['syllabus'] = syllabus
    # ...

    # ...
    if request.POST:
        syllabus.status = 'approved'
        syllabus.save()

        return redirect('accreditation:edit_syllabus', name=name, accreditation_name=accreditation_name)
    # ...

    return render(request, 'accreditation/approve_syllabus.html', context)
