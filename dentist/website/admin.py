from django.contrib import admin
from .models import Mumbai, Delhi, Chennai, Jaipur, Kolkata, All_Categories_Mumbai, User_Categories, User_Output

# Register your models here.
admin.site.register(Mumbai)
admin.site.register(All_Categories_Mumbai)
admin.site.register(User_Categories)
admin.site.register(User_Output)
admin.site.register(Delhi)
admin.site.register(Chennai)
admin.site.register(Jaipur)
admin.site.register(Kolkata)