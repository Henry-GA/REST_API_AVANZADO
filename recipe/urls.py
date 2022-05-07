from django.urls import URLPattern, path, include
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('tags', views.TagViewset)
router.register('ingrendients', views.IngredientsViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns=[
    path('', include(router.urls))
]