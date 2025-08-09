from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DepartmentViewSet, DelegationMatrixViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'delegation-matrix', DelegationMatrixViewSet, basename='delegationmatrix')

urlpatterns = [
    path('', include(router.urls)),
]