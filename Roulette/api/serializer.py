from rest_framework import serializers
from .models import Roulette, Bet


class RouletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roulette
        fields = "__all__"


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = "__all__"

    def validate(self, data):
        bet_type = data.get("bet_type")
        bet_value = data.get("bet_value")
        roulette = data.get("roulette")

        if not roulette.availability:
            raise serializers.ValidationError(
                {"message": "The roulette is not available."}
            )

        if bet_type == "number":
            if not bet_value.isdigit() or not (0 <= float(bet_value) <= 36):
                raise serializers.ValidationError(
                    {
                        "message": f"{bet_value} is not an allowed value. Use a value between 0 and 36."
                    }
                )

        elif bet_type == "color":
            if bet_value not in ["B", "R"]:
                raise serializers.ValidationError(
                    {"message": f"{bet_value} is not an allowed value. Use 'B', 'R'."}
                )

        return data
