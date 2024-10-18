from django.db import models
from categories.models import category
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# Conference model
class conference(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.FloatField()
    capacity = models.IntegerField(validators=[MaxValueValidator(900, message="Capacity must be under 900")])
    program = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'], message="Invalid file extension")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Fixed field name
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name="conferences")

    # Clean method to validate dates
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('End date must be greater than the start date')
        if self.start_date < timezone.now().date():
            raise ValidationError('The start date must be today or later')

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_date__gte=timezone.now().date()), name="start_date_gte_today")
        ]

    def __str__(self):
        return f"{self.title} ({self.start_date})"
