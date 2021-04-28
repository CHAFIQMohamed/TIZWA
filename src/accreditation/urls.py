from django.urls import path
from accreditation.views import create_accreditation_view
from accreditation.views import edit_accreditation_view
from accreditation.views import accreditation_view
from accreditation.views import detail_accreditation_view
from accreditation.views import create_syllabus_view
from accreditation.views import edit_accreditation_general_view
from accreditation.views import edit_accreditation_goals_view
from accreditation.views import edit_accreditation_areas_view
from accreditation.views import edit_accreditation_acquired_skills_view
from accreditation.views import edit_accreditation_careers_view
from accreditation.views import edit_accreditation_syllabus_view
from accreditation.views import edit_syllabus_view
from accreditation.views import edit_syllabus_goals_view
from accreditation.views import edit_syllabus_description_view
from accreditation.views import edit_syllabus_evaluation_view
from accreditation.views import edit_syllabus_grad_view
from accreditation.views import edit_syllabus_validation_view
from accreditation.views import edit_syllabus_general_view
from accreditation.views import edit_syllabus_intervention_view
from accreditation.views import ( detail_syllabus_view, 
                                  approve_syllabus_view, 
                                  request_approval_syllabus_view,
)

from accreditation.views import ( edit_accreditation_access_diploma_view,
                                  edit_accreditation_access_prerequisite_view,
                                  edit_accreditation_access_selection_view,
                                  edit_accreditation_access_file_view,
                                  edit_accreditation_access_exam_view,
                                  edit_accreditation_access_interview_view,
)

app_name = 'accreditation'

urlpatterns = [
    path('', accreditation_view, name="accreditation"),
    path('create', create_accreditation_view, name="create"),
    path('<name>/detail', detail_accreditation_view, name="detail_accreditation"),
    path('<name>/edit', edit_accreditation_view, name="edit_accreditation"),
    path('<name>/edit/general', edit_accreditation_general_view, name="edit_accreditation_general"),    
    path('<name>/edit/goals', edit_accreditation_goals_view, name="edit_accreditation_goals"),
    path('<name>/edit/areas', edit_accreditation_areas_view, name="edit_accreditation_areas"),
    path('<name>/edit/acquired_skills', edit_accreditation_acquired_skills_view, name="edit_accreditation_acquired_skills"),
    path('<name>/edit/careers', edit_accreditation_careers_view, name="edit_accreditation_careers"),
    path('<name>/edit/syllabus', edit_accreditation_syllabus_view, name="edit_accreditation_syllabus"),  

    path('<name>/edit/access/diploma', edit_accreditation_access_diploma_view, name="edit_accreditation_access_diploma"),
    path('<name>/edit/access/prerequisite', edit_accreditation_access_prerequisite_view, name="edit_accreditation_access_prerequisite"),
    path('<name>/edit/access/selection', edit_accreditation_access_selection_view, name="edit_accreditation_access_selection"),
    path('<name>/edit/access/file', edit_accreditation_access_file_view, name="edit_accreditation_access_file"),
    path('<name>/edit/access/exam', edit_accreditation_access_exam_view, name="edit_accreditation_access_exam"),
    path('<name>/edit/access/interview', edit_accreditation_access_interview_view, name="edit_accreditation_access_interview"),
    

    path('create_syllabus', create_syllabus_view, name="create_syllabus"), # TODO remove
    path('<accreditation_name>/<name>/syllabus', edit_syllabus_view, name="edit_syllabus"),    
    path('<accreditation_name>/<name>/syllabus/edit/goals', edit_syllabus_goals_view, name="edit_syllabus_goals"),
    path('<accreditation_name>/<name>/syllabus/detail', detail_syllabus_view, name="detail_syllabus"),
    path('<accreditation_name>/<name>/syllabus/approve', approve_syllabus_view, name="approve_syllabus"),
    path('<accreditation_name>/<name>/syllabus/request_approval', request_approval_syllabus_view, name="request_approval_syllabus"),

    path('<accreditation_name>/<name>/syllabus/edit/description', edit_syllabus_description_view, name="edit_syllabus_description"),
    path('<accreditation_name>/<name>/syllabus/edit/evaluation', edit_syllabus_evaluation_view, name="edit_syllabus_evaluation"),
    path('<accreditation_name>/<name>/syllabus/edit/grad', edit_syllabus_grad_view, name="edit_syllabus_grad"),
    path('<accreditation_name>/<name>/syllabus/edit/validation', edit_syllabus_validation_view, name="edit_syllabus_validation"),
    path('<accreditation_name>/<name>/syllabus/edit/general', edit_syllabus_general_view, name="edit_syllabus_general"),
    path('<accreditation_name>/<name>/syllabus/edit/intervention', edit_syllabus_intervention_view, name="edit_syllabus_intervention"),
 ]