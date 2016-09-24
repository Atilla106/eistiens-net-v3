from django.db import models


class SchoolYear(models.Model):
    """
    A model representing a school year. Only one is supposed to be created each
    year, so it can be used to reference everything year-related.
    """
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return "{}-{}".format(str(self.year), str(self.year + 1))
