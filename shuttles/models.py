from django.db import models
from django.core.validators import MinLengthValidator
from dashboard.models import Organization
from django.utils import timezone
import uuid

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

# Create your models here.
class Shuttle(models.Model):
    id_number = models.IntegerField(default=0)
    shuttle_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    vehicle_number = models.CharField(validators=[MinLengthValidator(4)], max_length=10)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_running = models.BooleanField(default=False)
    added_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.pk:
            all_shuttles = Shuttle.objects.filter(
                organization=self.organization
            ).count()
            self.id_number = all_shuttles + 1
        super(Shuttle, self).save(*args, **kwargs)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.vehicle_number} - {self.shuttle_id} - {self.id_number}"
