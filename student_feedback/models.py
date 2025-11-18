from django.db import models

class Feedback(models.Model):

    # Constants are useful, and easier to remember than the text used 
    PENDING = 'P'
    APPROVED = 'A'
    BLOCKED = 'B'

    # Dictionary of values that are stored in the database, 
    # and the human-readable equivalent, used when displaying a feedback in the admin console
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
        # Display 'anonymous' if the user does not enter an email 
        # Display no more than the first 50 characters of the text to save space in the string representation
        # The full text will be saved in the database and can be viewed in the details for an individual feedback in the admin console
        email = self.email if self.email else 'anonymous'
        return f'Text: {self.text[:50]}, Date: {self.date_submitted}, email: {email}, Status: {self.STATUS_CHOICES[self.status]}'
    


