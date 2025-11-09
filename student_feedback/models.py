from django.db import models
from datetime import datetime

class Feedback(models.Model):
    text = models.TextField(blank=False, max_length=1000)
    email = models.EmailField(blank=True, null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(null=False, default=False)

    def __str__(self):
        # Display the first 100 characters of the text to save space
        return f'Review Text: {self.text[:100]}, Date: {self.date_submitted}, Approved: {self.approved}'
    


