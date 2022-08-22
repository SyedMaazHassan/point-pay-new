from statistics import mode
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from dashboard.models import Organization
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

# paste in your models.py
def only_int(value):
    if value.isdigit() == False:
        raise ValidationError("PIN code format is: xxxx (only 4 digits are allowed)")


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

# Create your models here.
class Driver(models.Model):
    id_number = models.IntegerField(default=0)
    profile_picture = models.ImageField(
        upload_to="profile-pictures/drivers",
        default="profile-pictures/drivers/default-dp.png",
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # driver_cnic = models.IntegerField(null =True, blank=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    # driver_address = models.CharField(max_length=100, null =True, blank=True)
    pin = models.CharField(validators=[only_int, MinLengthValidator(4)], max_length=4)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )
    added_at = models.DateTimeField(default=timezone.now)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} - {self.id}"

    def save(self, *args, **kwargs):
        if not self.pk:
            all_drivers = Driver.objects.filter(organization=self.organization).count()
            self.id_number = all_drivers + 1
        if not self.profile_picture:
            self.profile_picture = "profile-pictures/drivers/default-dp.png"
        super(Driver, self).save(*args, **kwargs)

    class Meta:
        ordering = ("id",)




class DriverSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
