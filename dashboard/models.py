from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint
from itertools import chain
import qrcode
import datetime

# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver



class Organization(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=15, default="organization")
    abbr = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=15)
    logo = models.ImageField(upload_to="logo")
    point_fee = models.FloatField(default=500)
    founded_in = models.DateField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)

    def getJson(self):
        opts = self._meta
        opts.image_field
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            print(f)
            data[f.name] = f.value_from_object(self)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(self)]
        return data
        # return model_to_dict(self)

    def makeAbbr(self, name):
        name_list_form = name.split(" ")
        abbr = ""
        for single_word in name_list_form:
            abbr += single_word[0].upper()
        return abbr

    def save(self, *args, **kwargs):
        if not self.pk and not self.abbr:
            self.abbr = self.MakeAbbr(self.name)
        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.abbr}) {self.city}"


class Department(models.Model):
    abbr = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=50)
    added_at = models.DateTimeField(default=timezone.now)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class UserInfo(models.Model):
    uid = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        error_messages={"unique": "User with this UID number already exists."},
    )
    STATUS_CHOICES = [("student", "Student"), ("admin", "Admin")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="dp", default="dp/profile.jpg")
    phone = models.CharField(
        max_length=17,
        unique=True,
        null=True,
        blank=True,
        error_messages={"unique": "User with this phone number already exists."},
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)

    def validate_roll_no(self):
        if not self.roll_no:
            raise Exception("Roll no. is required")
        if "-" not in self.roll_no:
            raise Exception("Roll no. must be in correct format (CS-11001)")        
        all_dept_abbrs = Department.objects.filter(organization_id = self.organization_id).values_list("abbr", flat=True)
        roll_splited = self.roll_no.split("-")
        dept_part = roll_splited[0].upper()
        num_part = roll_splited[1]
        if dept_part not in all_dept_abbrs:
            raise Exception("Given department is not included in your university")
        if len(num_part) != 5:
            raise Exception("Roll no. must be in correct format (CS-11001)")
        current_timezone = timezone.now().year
        year_part = int(num_part[:2])
        number_part = int(num_part[2:])
        # if year_part > 


        

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.status} - {self.organization.abbr}"

    def save(self, *args, **kwargs):
        phone = self.phone
        if phone:
            phone = phone.replace("-", "")
            phone = phone.replace("+", "")
            if not (phone.isnumeric() and (9 < len(phone) < 17)):
                raise Exception("Given phone number is not valid")

        super(UserInfo, self).save(*args, **kwargs)

    def getJson(self):
        student_info = {
            "id": self.pk,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "full_name": f"{self.user.first_name} {self.user.last_name}",
            "profile_picture": str(self.profile_picture),
        }
        return student_info

    def isVoucherAlreadyCreated(self):
        current_date = timezone.now()
        check_voucher_query = Voucher.objects.filter(
            organization=self.organization,
            month=current_date.month,
            year=current_date.year,
        ).order_by("-created_at")
        if check_voucher_query.exists():
            # returning last recent voucher
            return check_voucher_query[0]
        else:
            return False


class Voucher(models.Model):
    price = models.FloatField()
    code = models.CharField(max_length=255, null=True)
    month = models.IntegerField(default=1)
    year = models.IntegerField()
    qr_code_picture = models.ImageField(upload_to="qr", null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        month = datetime.date(1900, self.month, 1).strftime("%b")
        return f"{month} {self.year} - Rs.{self.price} - Expired: {self.is_expired}"

    def dateDict(self):
        return {
            "MONTH": datetime.date(1900, self.month, 1).strftime("%B"),
            "month": datetime.date(1900, self.month, 1).strftime("%b"),
            "year": self.year,
        }

    def showDate(self):
        month = datetime.date(1900, self.month, 1).strftime("%b")
        return f"{month}, {self.year}"

    def expireIt(self):
        # get current month and year
        current_date = timezone.now()
        month = current_date.month
        year = current_date.year
        if (self.year <= year) and self.month < month:
            self.is_expired = True
            self.save()

    def generateCode(self):
        length = 64
        """
        This function will return a string of random
        alphanumeric code of given length (integer)
        """
        CHAR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        code = ""
        for i in range(0, length):
            index = randint(0, len(CHAR) - 1)
            code += CHAR[index]
        return code

    def generate_qrcode(self):
        import time
        from io import BytesIO
        from django.core.files import File
        from PIL import Image, ImageDraw, ImageOps
        from django.conf import settings
        import os

        base_path = settings.BASE_DIR

        logo_path = os.path.join(base_path, "media", str(self.organization.logo))

        logo2 = Image.open(logo_path).convert("RGBA")
        # logo2.convert("1")
        # logo2 = self.add_corners(logo2, 100)
        # logo2 = ImageOps.grayscale(logo2)

        logo = Image.new("RGBA", logo2.size, "WHITE")
        logo.paste(logo2, mask=logo2)

        # taking base width
        basewidth = 120

        # adjust image size
        wpercent = basewidth / float(logo.size[0])
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

        # return None
        qrcode_image = qrcode.make(self.code)

        # qrcode_image = qrcode_image.convert('RGB')

        pos = (
            (qrcode_image.size[0] - logo.size[0]) // 2,
            (qrcode_image.size[1] - logo.size[1]) // 2,
        )

        qrcode_image.paste(logo, pos)

        qrcode_image.save(os.path.join(base_path, "media", "practise.png"))

        canvas = Image.new(
            "RGB", (qrcode_image.pixel_size, qrcode_image.pixel_size), "white"
        )

        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)

        filename = f"qr-code-{time.time()}.png"
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.qr_code_picture.save(filename, File(buffer), save=False)
        canvas.close()

    def setDefaultValues(self):
        current_date = timezone.now()
        self.price = self.organization.point_fee
        self.month = current_date.month
        self.year = current_date.year
        self.code = self.generateCode()
        self.generate_qrcode()
        self.save()

    def getJson(self):
        return {
            "price": f"Rs. {self.price}",
            "code": self.code,
            "month": datetime.date(1900, self.month, 1).strftime("%b"),
            "year": self.year,
            "qr_code": str(self.qr_code_picture.url),
            "is_expired": self.is_expired,
        }

    class Meta:
        ordering = ("-created_at",)


class Point(models.Model):
    vehicle_name = models.CharField(max_length=10)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.vehicle_name


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver
