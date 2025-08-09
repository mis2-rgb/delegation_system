from rest_framework import serializers
from .models import Organization, User
from organizations.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'department']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        organization = self.context['request'].user.organization if self.context['request'].user.is_authenticated else None
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            organization=organization,
            role=validated_data.get('role', User.Role.DOER),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user