from django.db import models


from autoslug import AutoSlugField
from django_countries.fields import CountryField
from django.urls import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from star_ratings.models import Rating
from model_utils.models import TimeStampedModel


class Cheese(TimeStampedModel):

    class Firmness(models.TextChoices):
        UNSPECIFIED = "unspecified", "Unspecified"
        SOFT = "soft", "Soft"
        SEMI_SOFT = "semi-soft", "Semi-Soft"
        SEMI_HARD = "semi-hard", "Semi-Hard"
        HARD = "hard", "Hard"


    name = models.CharField("Name of Cheese", max_length=255)
    slug = AutoSlugField(
        "Cheese address",
        unique=True,
        always_update=False,
        populate_from="name"
    )

    description = models.TextField("Description", blank=True)

    firmness = models.CharField("Firmness", max_length=20,
                               choices=Firmness.choices, default=Firmness.UNSPECIFIED)

    country_of_origin = CountryField("Country of Origin", blank=True)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )

    def get_absolute_url(self):
        return reverse("cheeses:detail", kwargs={"slug": self.slug})


    @property 
    def average_rating(self):

        ratings = Rating.objects.all().filter(cheese=self)
        if ratings is None:
            return 0
    
        total = 0
        count = 0

        for r in ratings:
            total += r.i_rating
            count += 1

        if count <= 0:
            return 0
    
        return total // count


class Rating (models.Model):
  i_rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator (1), MaxValueValidator(5)])

  creator = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    null=True, 
    on_delete=models.SET_NULL
    )
  
  cheese = models.ForeignKey(
     Cheese,
     null=True,
     on_delete=models.SET_NULL

  )

  def __str__(self):
      return f"{self.i_rating}"
