from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from account.forms import RegistrationForm
from account.forms import AccountAuthentificationForm
from account.forms import AccountUpdateForm

# =======================================================
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)

            return redirect('dashboard:home')
        else:
            context['registration_form'] = form

    else: # GET request
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)

# =======================================================
def logout_view(request):
    logout(request)
    return redirect('dashboard:home')

# =======================================================
def login_view(request):
    context = {}

    user = request.user
    if request.POST:
        form = AccountAuthentificationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('dashboard:home')

    else:
        form = AccountAuthentificationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)

# =======================================================
def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    print(">>> 1")
    print(request.POST)
    if request.POST:
        print(">>> 2")
        form = AccountUpdateForm(request.POST, instance=request.user)
        print(">>> 3")
        if form.is_valid():
            print(">>> 4")
            form.initial = {'identity_number': request.POST['identity_number'],
                            'identity_number': request.POST['identity_number'],
                            'tel': request.POST['tel'],
                            'address_home': request.POST['address_home'],
                            'address_city': request.POST['address_city'],
                            'address_postal_code': request.POST['address_postal_code'],
                            'address_country': request.POST['address_country'],
                            'profile': request.POST['profile'],
                            'grad': request.POST['grad'],
                            'expertize': request.POST['expertize'],
                            'university': request.POST['university'],
                            'departement': request.POST['departement'],
                            }
            print(">>> 5")
            form.save()
            print(">>> 6")
            context['success_message'] = "Updated"
        else:
            print(">>> NOT VALID")
    else:
        print(">>> NO POST")
        form = AccountUpdateForm(initial={'identity_number': request.user.identity_number,
                                          'identity_number': request.user.identity_number,
                                          'tel': request.user.tel,
                                          'address_home': request.user.address_home,
                                          'address_city': request.user.address_city,
                                          'address_postal_code': request.user.address_postal_code,
                                          'address_country': request.user.address_country,
                                          'profile': request.user.profile,
                                          'grad': request.user.grad,
                                          'expertize': request.user.expertize,
                                          'university': request.user.university,
                                          'departement': request.user.departement,
                                         })

    context['account_form'] = form

    return render(request, 'account/account.html', context)

# =======================================================
def must_authenticate_view(request):
    context = {}
    return render(request, 'account/must_authenticate.html', context)
