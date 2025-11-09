from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ['approved']

admin.site.register(Feedback, FeedbackAdmin)
