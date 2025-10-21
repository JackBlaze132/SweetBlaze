from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('promo', 'Promotion'),
        ('info', 'Information'),
        ('alert', 'Alert'),
    ]

    title = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.title