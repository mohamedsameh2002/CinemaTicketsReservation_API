
from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router=DefaultRouter()
router.register('geusts',views.viewsets_guest)
router.register('movies',views.viewsets_movie)
router.register('reservation',views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('django/nomodel/', views.no_rest_no_model),
    #2
    path('django/withmodel/', views.no_rest_from_model),

    #3.1 GET POST from rest framework function based view @api_view
    path('rest/fbv/', views.FBV_List),
    #3.2 DELETE PUT from rest framework function based view @api_view
    path('rest/fbv_pk/<int:pk>/', views.FBV_PK),

    #4.1 GET POST from rest framework class based view APIView
    path('rest/cbv/', views.CBV_List.as_view()),
    #4.2 DELETE PUT from rest framework  class based view APIView
    path('rest/cbv_pk/<int:pk>/', views.CBV_PK.as_view()),

    #5.1 GET POST from rest framework class based view Mixins
    path('rest/mixins/', views.mixins_list.as_view()),
    #5.2 DELETE PUT from rest framework  class based view Mixins
    path('rest/mixins/<int:pk>/', views.mixins_pk.as_view()),

    #6.1 GET POST from rest framework class based view Generic
    path('rest/generic/', views.generics_list.as_view()),
    #6.2 DELETE PUT from rest framework  class based view Generic
    path('rest/generic/<int:pk>/', views.generics_pk.as_view()),

    #7.Viewsets
    path('rest/viewsets/', include(router.urls)),

    #-----
    #8.find movie
    path('fbv/findmovie/', views.find_movie),

    #9. create new reservation
    path('fbv/newreservation/', views.new_reservation),



    #10.rest auth url
    path('api-auth/', include('rest_framework.urls')),

    #11.token authantication
    path('api-token-auth/', obtain_auth_token),






]
