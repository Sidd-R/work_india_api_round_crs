from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import CarSerializer, TransactionSerializer
from .models import Car, Transaction
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(["GET"])
def get_cars(request):
    try:
        origin = request.GET.get("origin", "Mumbai")
        destination = request.GET.get("destination", "Banglore")
        required_hours = int(request.GET.get("required_hours", 3))
    except ValueError:
        return Response({"error": "Invalid input"}, 400)

    cars = Car.objects.filter(current_city=origin)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    authentication_classes = [JWTAuthentication]

    # custom post
    def get_permissions(self):
        if self.action == "list":
            permission_classes = []
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        try:
            origin = self.request.query_params.get("origin", "Mumbai")
            destination = self.request.query_params.get("destination", "Banglore")
            required_hours = int(self.request.query_params.get("required_hours", 3))
        except ValueError:
            return Response({"error": "Invalid input"}, 400)
        
        cars = Car.objects.filter(current_city=origin)
        serializer = CarSerializer(cars, many=True)
        
        print(serializer)
        
        return Response(serializer.data)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        car = Car.objects.get(id=response.data["car_id"])
        car.is_available = False
        car.save()
        return response
