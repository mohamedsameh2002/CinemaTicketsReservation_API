from django.shortcuts import get_object_or_404
from django.http import JsonResponse,Http404
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import status,filters
from rest_framework.views import APIView
from rest_framework import generics,mixins,viewsets
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#1.without REST and model qurey
def no_rest_no_model(request):
    guests=[
        {
            'id':1,
            'Name':'Omar',
            'mobile':54684,
        },
        {
            'id':2,
            'Name':'mohamed',
            'mobile':146841,
        }
    ]
    return JsonResponse(guests,safe=False)


#2.#1.without REST with model qurey
def no_rest_from_model(request):
    data=Guest.objects.all()
    response={
        'guests':list(data.values('name','mobile'))

    }
    return JsonResponse(response)



#3.Function based views
#3.1 GET POST
@api_view(['GET','POST'])
def FBV_List(request):
    #GET
    if request.method == 'GET':
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    #POST 
    elif request.method == 'POST':
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            all_data=GuestSerializer(Guest.objects.all(),many=True).data
            return Response(data=all_data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.data,status=status.HTTP_400_BAD_REQUEST)


#3.2 PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_PK(request,pk):
    guest=guest=get_object_or_404(Guest,pk=pk)
    #GET
    if request.method == 'GET':
        serializer=GuestSerializer(guest,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    #PUT 
    elif request.method == 'PUT':
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    #DELETE 
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#4.CBV Class based views
#4.1 List and Create == GET and POST
class CBV_List (APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            all_data=GuestSerializer(Guest.objects.all(),many=True).data
            return Response(data=all_data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.data,status=status.HTTP_400_BAD_REQUEST)
        

#4.2 GET and PUT and DELETE -- CBV PK
class CBV_PK (APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        serializer=GuestSerializer(self.get_object(pk),many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    

    def put(self,request,pk):
        serializer=GuestSerializer(self.get_object(pk),data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#5.Mixins
#5.1 mixins list
class mixins_list(
mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request):
        return self.list(request)
    def post (self,request):
        return self.create(request)
    
#5.2 mixins get put delete
class mixins_pk(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request , pk):
        return self.retrieve(request)
    def put (self,request , pk):
        return self.update(request)
    def delete (self,request , pk):
        return self.destroy(request)
    
#6.Generics'
#6.1.get and post
class generics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]


#6.2 get put and delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    # authentication_classes=[BasicAuthentication]
    # permission_classes=[IsAuthenticated]





#7.Viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer


class viewsets_movie(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['movie']


class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class=ReservationSerializer

#--------

#8.Find movie
@api_view(['GET'])
def find_movie(request):
    movie=Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )
    serializer=MovieSerializer(movie,many=True)
    return Response(serializer.data)


#9. create new reservation
@api_view(['POST'])
def new_reservation(request):
    movie=Movie.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )
    guest=Guest()
    guest.name=request.data['name']
    guest.mobile=request.data['mobile']
    guest.save()
    reservation=Reservation()
    reservation.guest=guest
    reservation.movie=movie
    reservation.save()
    return Response(status=status.HTTP_201_CREATED)


