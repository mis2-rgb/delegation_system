from rest_framework import serializers
from .models import Department, DelegationMatrix


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class DelegationMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = DelegationMatrix
        fields = ['id', 'department', 'delegator', 'doer']

    def create(self, validated_data):
        user = self.context['request'].user
        instance = DelegationMatrix.objects.create(organization=user.organization, **validated_data)
        return instance