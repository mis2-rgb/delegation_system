from rest_framework import serializers
from .models import Task, TaskCompletion
from organizations.models import DelegationMatrix


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ['delegation_id', 'organization', 'delegator', 'created_at', 'updated_at', 'regenerated_count']
        fields = ['id', 'delegation_id', 'delegator', 'department', 'doer', 'description', 'complete_by', 'priority', 'attachment_image', 'attachment_file', 'created_at', 'updated_at', 'regenerated_count']

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        org = user.organization
        if not DelegationMatrix.objects.filter(organization=org, department=attrs['department'], delegator=user, doer=attrs['doer']).exists():
            raise serializers.ValidationError('Delegator is not allowed to assign this doer in this department.')
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        org = user.organization
        task = Task(**validated_data)
        task.organization = org
        task.delegator = user
        task.delegation_id = self.generate_delegation_id(org)
        task.save()
        return task

    def generate_delegation_id(self, org):
        from django.utils.crypto import get_random_string
        while True:
            candidate = get_random_string(10).upper()
            if not Task.objects.filter(organization=org, delegation_id=candidate).exists():
                return candidate


class TaskCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCompletion
        read_only_fields = ['completed_by', 'completed_at', 'verified_by', 'verified_at', 'is_accepted', 'quality_issue']
        fields = ['id', 'task', 'completed_by', 'completed_at', 'proof_image', 'proof_file', 'remarks', 'quality_issue', 'verified_by', 'verified_at', 'is_accepted']

    def create(self, validated_data):
        request = self.context['request']
        completion = TaskCompletion(**validated_data)
        completion.completed_by = request.user
        completion.save()
        return completion