from django.contrib import admin
from .models import conference
from .models import participants
from .models import reservation

#admin.site.register(conference) 
admin.site.register(participants) 
admin.site.register(reservation) 



# Register your models here.
