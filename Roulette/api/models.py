from django.db import models
from django.core.validators import MaxValueValidator, ValidationError


def validate_bet_type(value):
    if value not in ["number", "color"]:
        raise ValidationError(
            f"{value} is not an allowed value. Use 'number' or 'color'."
        )


class Roulette(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    availability = models.BooleanField(default=False)
    bet_close = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "roulette"


class Bet(models.Model):
    roulette = models.ForeignKey(Roulette, models.CASCADE, null=False)
    bet_user = models.CharField(max_length=30, blank=False, null=False)
    bet_type = models.CharField(
        max_length=10, blank=False, null=False, validators=[validate_bet_type]
    )
    bet_value = models.CharField(max_length=2, blank=False, null=False)
    fee = models.FloatField(null=False, validators=[MaxValueValidator(10000)])

    class Meta:
        managed = False
        db_table = "bet"


class Winer(models.Model):
    bet = models.ForeignKey(Bet, models.DO_NOTHING, null=False)
    earned = models.FloatField(null=False)

    class Meta:
        managed = False
        db_table = "winer"
