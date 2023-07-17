from django.db import models

# Create your models here.
from django.db import models


class Notification(models.Model):
    PENDING = 1
    SENT = 2
    ERROR = 3
    STATUSES = (
        (PENDING, 'Pending'),
        (SENT, 'Sent'),
        (ERROR, 'Error'),
    )
    telegram_id = models.CharField(max_length=50)
    text = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    answer_time = models.DurationField()
    status = models.IntegerField(choices=STATUSES, default=PENDING, verbose_name='Статус')

    def __str__(self):
        return f"Notification for {self.telegram_id} - Test: {self.text}"