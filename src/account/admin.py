from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account

# =======================================================
class AccountAdmin(UserAdmin):
    list_display = (
                    # common informations
                    'email',
                    'username',
                    'last_name',
                    'first_name',
                    'date_joined',
                    'last_login',
                    # professor
                    'profile',
                    'grad',
                    'expertize',
                    'university',
                    'tel',                    
                    # flags
                    'is_admin',
                    'is_active',
                    'is_staff',
                    'is_student',
                    'is_professor',
                   )

    search_fields = ('email', 'username', 'last_name', 'first_name') # TODO add grad, expertize and others
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# =======================================================
admin.site.register(Account, AccountAdmin)
