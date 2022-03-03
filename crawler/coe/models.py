from django.db import models

# Create your models here.

class Competition(models.Model):
    country = models.CharField(max_length=100)
    year = models.CharField(max_length=100)

    def __str__(self):
        return f"<Competition (country: {country}, year: {year})>"


class Result(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    rank = models.IntegerField()
    score = models.FloatField()
    farmer_or_representative = models.CharField(max_length=100)
    farm_or_cws = models.CharField(max_length=100)
    farm_url = models.CharField(max_length=100)

    def __str__(self):
        return (
            f"<Result ("
            f"rank: {self.rank}, "
            f"score: {self.score}, "
            f"farmer_or_representative: {self.farmer_or_representative}, "
            f"farm_or_cws: {self.farm_or_cws}, "
            f"farm_url: {self.farm_url}, "
            f"competition: {self.competition}"
            f")>"
        )
