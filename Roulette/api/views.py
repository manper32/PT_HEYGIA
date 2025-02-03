from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Roulette, Bet, Winer
from .serializer import RouletteSerializer, BetSerializer
import random


class RouletteViewSet(viewsets.ModelViewSet):
    queryset = Roulette.objects.all()
    serializer_class = RouletteSerializer

    @action(detail=True, methods=["get"])
    def validate_status(self, request, pk=None):
        roulette = get_object_or_404(Roulette, pk=pk)

        if roulette.availability:
            return Response({"message": "Allow"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Denied"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["post"])
    def close_bets(self, request, pk=None):
        try:
            roulette = self.get_object()
            print(roulette.bet_close)
            if roulette.bet_close != False:
                return Response(
                    {
                        "message": "The Roulette must be open, field 'bet_close' = false."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # random_number = random.randint(0, 36)
            random_number = 1
            color = "R" if random_number % 2 == 0 else "B"

            winning_bets = Bet.objects.filter(
                Q(roulette=roulette, bet_type="color", bet_value=color)
                | Q(roulette=roulette, bet_type="number", bet_value=str(random_number))
            )

            COLOR_MULTIPLIER = 1.8
            NUMBER_MULTIPLIER = 5

            winning_bets_data = [
                {
                    "id": bet.id,
                    "bet_type": bet.bet_type,
                    "bet_value": bet.bet_value,
                    "fee": bet.fee,
                    "earned": round(
                        (
                            bet.fee
                            * (
                                COLOR_MULTIPLIER
                                if bet.bet_type == "color"
                                else NUMBER_MULTIPLIER
                            )
                        ),
                        2,
                    ),
                    "roulette": bet.roulette.id,
                }
                for bet in winning_bets
            ]

            load_data = [
                Winer(
                    bet=bet,
                    earned=round(
                        (
                            bet.fee
                            * (
                                COLOR_MULTIPLIER
                                if bet.bet_type == "color"
                                else NUMBER_MULTIPLIER
                            )
                        ),
                        2,
                    ),
                )
                for bet in winning_bets
            ]

            Winer.objects.bulk_create(load_data)

            roulette.bet_close = True
            roulette.save()

            return Response(
                {
                    "message": "closed bets.",
                    "value": random_number,
                    "records": winning_bets_data,
                },
                status=status.HTTP_200_OK,
            )

        except Roulette.DoesNotExist:
            return Response(
                {"message": "Roulette not found."}, status=status.HTTP_404_NOT_FOUND
            )


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
