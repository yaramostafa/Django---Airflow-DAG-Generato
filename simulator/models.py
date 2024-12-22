from django.db import models

# Create your models here.
class Simulator(models.Model):
    start_date = models.DateTimeField()
    interval = models.CharField(max_length=50)  # e.g., 'daily', 'hourly'
    kpi_id = models.IntegerField()

    def __str__(self):
        return f"Simulator {self.id}"
