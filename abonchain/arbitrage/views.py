import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .arbitrage_bot.arbitrage_bot import run_arbitrage_bot_task
from .models import ArbitrageOpportunity
from .serializers import ArbitrageOpportunitySerializer


def run_arbitrage_bot(request):
    try:
        logging.info("Starting the arbitrage bot.")

        while True:
            # Call the Celery task asynchronously
            result = run_arbitrage_bot_task.apply_async()

            # Log successful completion
            logging.info(
                "Arbitrage bot started successfully with Task ID: %s",
                result.id,
            )

            # Return a response with status and task ID (result)
            return JsonResponse(
                {
                    "status": "success",
                    "task_id": result.id,
                    "message": "Arbitrage bot is running.",
                },
            )

    except Exception as e:
        # Log any errors
        logging.exception("Arbitrage bot error, exception: %s")

        # Return error response
        return JsonResponse(
            {
                "status": "error",
                "message": str(e),
            },
        )


class ArbitrageOpportunityListView(APIView):
    def get(self, request):
        opportunities = ArbitrageOpportunity.objects.all().order_by("-timestamp")
        serializer = ArbitrageOpportunitySerializer(opportunities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArbitrageOpportunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
