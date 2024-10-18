from django.db import models
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
# Create your models here.

def validate_letters_only(value):
    if not re.match(r'^[A-Za-z\s]+$',value):
        raise ValidationError('this field should only contain letters')

class category(models.Model):
    letter_only=RegexValidator(r'^[A-Za-z\s]+$','ONLY letter are allowed')
    title=models.CharField(max_length=255, validators=[validate_letters_only])
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural="categories"