from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from .models import Car, Owner, VehicleHistory, CarImage
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.response import Response

from .permissions import CustomDjangoModelPermissions
from .serializers import CarSerializer, OwnerSerializer, VehicleHistorySerializer, CarImageSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


def index(request):
    return HttpResponse("Hejka naklejka")

# class CarDetail(APIView):
#     authentication_classes = [BearerTokenAuthentication]
#     permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
#
#     def get_queryset(self):
#         return Car.objects.all()
#
#     def get_object(self, pk):
#         try:
#             return Car.objects.get(pk=pk)
#         except Car.DoesNotExist:
#             raise NotFound(detail="Car not found", code=404)
#
#     def get(self, request, pk, format=None):
#         car = self.get_object(pk)
#         serializer = CarSerializer(car)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         car = self.get_object(pk)
#         serializer = CarSerializer(car, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         team = self.get_object(pk)
#         team.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#logowanie
class CustomAuthTokenLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username' : user.username,
        })

#samochody cena>price
@api_view(['GET'])
def pricegt(request, price):
    cars = Car.objects.filter(price__gt=price)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

#samochody cena<price
@api_view(['GET'])
def pricelt(request, price):
    cars = Car.objects.filter(price__lt=price)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

#rejestracja nowego uzytkownika
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not (username and email and password):
            return Response({'error': 'Wymagane są wszystkie pola: username, email, password'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username, email, password)
        return Response({'message': 'Użytkownik został zarejestrowany'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#lista wszystkich obiektow modelu Car
@api_view(['GET'])
def car_list(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

#dane poszczegolnego samochodu
@api_view(['GET'])
def get_car(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        return Response(serializer.data)

#Aktualizacja danych samochodu.
@api_view(['PUT'])
def update_car(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#usuwanie samochodu
@api_view(['DELETE'])
def delete_car(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#tworzenie samochodu
@api_view(['POST'])
def create_car(request):
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create_owner(request):
    if request.method == 'POST':
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_owner(request, pk):
    try:
        owner = Owner.objects.get(pk=pk)
    except Owner.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OwnerSerializer(owner)
    return Response(serializer.data)

@api_view(['PUT'])
def update_owner(request, pk):
    try:
        owner = Owner.objects.get(pk=pk)
    except Owner.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OwnerSerializer(owner, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_owner(request, pk):
    try:
        owner = Owner.objects.get(pk=pk)
        owner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Owner.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_vehicle_history(request):
    serializer = VehicleHistorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_vehicle_history(request, pk):
    try:
        vehicle_history = VehicleHistory.objects.get(pk=pk)
    except VehicleHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = VehicleHistorySerializer(vehicle_history)
    return Response(serializer.data)

@api_view(['PUT'])
def update_vehicle_history(request, pk):
    try:
        vehicle_history = VehicleHistory.objects.get(pk=pk)
    except VehicleHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = VehicleHistorySerializer(vehicle_history, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_vehicle_history(request, pk):
    try:
        vehicle_history = VehicleHistory.objects.get(pk=pk)
        vehicle_history.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except VehicleHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_car_image(request):
    serializer = CarImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_car_image(request, pk):
    try:
        car_image = CarImage.objects.get(pk=pk)
    except CarImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CarImageSerializer(car_image)
    return Response(serializer.data)

@api_view(['PUT'])
def update_car_image(request, pk):
    try:
        car_image = CarImage.objects.get(pk=pk)
    except CarImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CarImageSerializer(car_image, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_car_image(request, pk):
    try:
        car_image = CarImage.objects.get(pk=pk)
        car_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except CarImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)