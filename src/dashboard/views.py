from django.shortcuts import render

from notifications.models import Notification

from accreditation.models import Accreditation

def index_view(request):
    context = {}
    return render(request, 'dashboard/index.html', context)

def home_dashboard_view(request):
    context = {}

    # ...
    accreditations = Accreditation.objects.all()
    context['accreditations'] = accreditations
    # ...

    # ... we need the try/except because of the superuser
    #     TODO improve, try/except is time consuming
    try:
        #notifications = Notification.objects.unread()
        notifications = request.user.notifications.unread()

        context['notifications'] = notifications
    except:
        pass
    # ...

    return render(request, 'dashboard/home.html', context)

def new_dashboard_view(request):
    context = {}
    return render(request, 'dashboard/new.html', context)
