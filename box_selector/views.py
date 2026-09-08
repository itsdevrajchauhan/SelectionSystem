from django.shortcuts import get_object_or_404

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import BoxRecommendationSerializer
from .services import find_best_box


class BoxRecommendationView(APIView):

    def post(self, request):
        serializer = BoxRecommendationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(
            Product,
            id=serializer.validated_data["product_id"],
        )

        box = find_best_box(product)

        if box is None:
            return Response(
                {"detail": "No suitable box found."},
                status=400,
            )

        return Response(
            {
                "box_id": box.id,
                "box_name": box.name,
                "cost": box.cost,
            }
        )