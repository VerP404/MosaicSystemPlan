from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Plan
from .serializers import PlanSerializer


class PlanListView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)
