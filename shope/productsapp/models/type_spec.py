from django.db import models
from coreapp.models import BaseModel
from productsapp.models.category import Category


class TypeSpecific(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=True)
    category = models.ManyToManyField(Category, related_name="type_spec")

    def __str__(self):
        return self.name
