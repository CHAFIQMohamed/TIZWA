import string
import random

from mdutils.mdutils import MdUtils


from accreditation.models import Accreditation
from accreditation.models import Syllabus

#==============================================================================
def random_string( n ):
    chars    = string.ascii_uppercase + string.ascii_lowercase
    selector = random.SystemRandom()
    return ''.join( selector.choice( chars ) for _ in range( n ) )

# ====================================
# TODO avoid saving/reading in/from a file
def model_to_md(model, level=1):

    # ...
    if isinstance(model, Accreditation):
        title = '{name}. {title}'.format(name=model.name, title=model.title)

    elif isinstance(model, Syllabus):
        title = '{name}. {title}'.format(name=model.name, title=model.title)

    else:
        raise NotImplementedError('{} not available'.format(type(model)))
    # ...

    md = MdUtils(title=title)

    # ...
    if isinstance(model, Accreditation):
        _accreditation_to_md(model, md, level)

    elif isinstance(model, Syllabus):
        _syllabus_to_md(model, md, level)

    else:
        raise NotImplementedError('{} not available'.format(type(model)))
    # ...

    # TODO Create a table of contents
#    mdFile.new_table_of_contents(table_title='Contents', level=2)

    return {'data': md.data, 'toc': md.toc}

# ====================================
def _accreditation_to_md(model, md, level):
    # ... write description
    md.new_header(level=level, title='Identification de la filière')

    # intitulé
    line = "**Intitulé**: {title} ({name})".format(title=model.title, name=model.name)
    md.new_line(line)

    # Disciplines 
    text = model.domains # TODO improve add ','
    if not text:
        text = ""
    line = "**Disciplines**: {}".format(text)
    md.new_line(line)

    # intitulé
    text = model.options # TODO add ',' between options?
    if not text:
        text = ""
    line = "**Options**: {}".format(text)
    md.new_line(line)

    # Diplôme délivré
    if model.kind.lower() == 'master':
        text = "2 ans après BAC + 3"

    else:
        raise ValueError('{} not available'.format(model.kind))

    line = "**Diplôme délivré**: {}".format(text)
    md.new_line(line)

    # Spécialité(s) du Diplôme  
    text = model.specialty1
    if model.specialty2:
        text = "{text}, {new}".format(text=text, new=model.specialty2) # TODO improve use list
    if model.specialty3:
        text = "{text}, {new}".format(text=text, new=model.specialty3) # TODO improve use list
    if model.specialty4:
        text = "{text}, {new}".format(text=text, new=model.specialty4) # TODO improve use list

    line = "**Spécialité(s) du Diplôme**: {}".format(text)
    md.new_line(line)

    # Mots Clés 
    text = model.keywords # TODO improve add ','
    if not text:
        text = ""
    line = "**Mots Clés**: {}".format(text)
    md.new_line(line)        
    # ...
    
    # Objectifs de la formation
    md.new_header(level=level, title='Objectifs de la formation')
    if model.goals:
        md.new_paragraph(model.goals)
    
    # Compétences à acquérir
    md.new_header(level=level, title='Compétences à acquérir')
    if model.acquired_skills:
        md.new_paragraph(model.acquired_skills)

    # Débouchés de la formation
    md.new_header(level=level, title='Débouchés de la formation')
    if model.careers:
        md.new_paragraph(model.careers)

    # ... Conditions d’accès et pré-requis
    md.new_header(level=level, title='Conditions d’accès et pré-requis')

    # Diplômes requis
    md.new_header(level=level+1, title='Diplômes requis')
    if model.access_diploma:
        md.new_paragraph(model.access_diploma)

    # Pré requis pédagogiques spécifiques
    md.new_header(level=level+1, title='Pré requis pédagogiques spécifiques')
    if model.access_prerequisite:
        md.new_paragraph(model.access_prerequisite)

    # Procédures de sélection
    md.new_header(level=level+1, title='Procédures de sélection')
    if model.access_selection:
        md.new_paragraph(model.access_selection)

    # Etude du dossier
    md.new_header(level=level+1, title='Etude du dossier')
    if model.access_file:
        md.new_paragraph(model.access_file)

    # Test écrit
    md.new_header(level=level+1, title='Test écrit')
    if model.access_exam:
        md.new_paragraph(model.access_exam)

    # Entretien
    md.new_header(level=level+1, title='Entretien')
    if model.access_interview:
        md.new_paragraph(model.access_interview)
    # ...

    # write articulation
    #md.new_header(level=level, title='articulation')
    #md.new_paragraph(model.articulation)

# ====================================
def _syllabus_to_md(model, md, level):
    # write goals
    md.new_header(level=level, title='Goals')
    if model.goals:
        md.new_paragraph(model.goals)
    
    # write description
    md.new_header(level=level, title='Description')
    if model.description:
        md.new_paragraph(model.description)

    # write evaluation
    md.new_header(level=level, title='evaluation')
    if model.evaluation:
        md.new_paragraph(model.evaluation)

    # write grad
    md.new_header(level=level, title='grad')
    if model.grad:
        md.new_paragraph(model.grad)

    # write validation
    md.new_header(level=level, title='validation')
    if model.validation:
        md.new_paragraph(model.validation)