from django.contrib import admin
from .models import Mumbai, Delhi, Chennai, Jaipur, Kolkata
from .models import All_Categories_Mumbai, All_Categories_Delhi, All_Categories_Jaipur, All_Categories_Kolkata, All_Categories_Chennai
from .models import Mumbai_User_Output, Delhi_User_Output, Jaipur_User_Output, Kolkata_User_Output, Chennai_User_Output
from .models import User_Categories, User_Output

# Register your models here.
admin.site.register(Mumbai_User_Output)
admin.site.register(Delhi_User_Output)
admin.site.register(Jaipur_User_Output)
admin.site.register(Kolkata_User_Output)
admin.site.register(Chennai_User_Output)
admin.site.register(All_Categories_Mumbai)
admin.site.register(All_Categories_Delhi)
admin.site.register(All_Categories_Jaipur)
admin.site.register(All_Categories_Kolkata)
admin.site.register(All_Categories_Chennai)
admin.site.register(User_Categories)
admin.site.register(User_Output)
admin.site.register(Mumbai)
admin.site.register(Delhi)
admin.site.register(Chennai)
admin.site.register(Jaipur)
admin.site.register(Kolkata)