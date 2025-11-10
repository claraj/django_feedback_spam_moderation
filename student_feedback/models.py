from django.db import models
from datetime import datetime

class Feedback(models.Model):

    PENDING = 'P'
    APPROVED = 'A'
    BLOCKED = 'B'

    # Dictionary of values that are stored in the database and the human-readable equivalent
    STATUS_CHOICES = {
        PENDING: 'Pending',
        APPROVED: 'Approved',
        BLOCKED: 'Blocked'
    }

    text = models.TextField(blank=False, max_length=1000)
    email = models.EmailField(blank=True, null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=False, blank=False, max_length=2, default=PENDING, choices=STATUS_CHOICES)

    def __str__(self):
        # Display the first 100 characters of the text to save space
        return f'Review Text: {self.text[:100]}, Date: {self.date_submitted}, Status: {self.STATUS_CHOICES[self.status]}'
    


