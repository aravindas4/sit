from rest_framework import serializers
from simple import models as simple_models


class IssueSerializer(serializers.ModelSerializer):
    assigned_to = serializers.ReadOnlyField(source='assigned_to.username')
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = simple_models.Issue
        fields = ('id', 'title', 'description', 'assigned_to', 'created_by', 'status',)


class UserSerializer(serializers.ModelSerializer):
    issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = simple_models.MyUser
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'access_token', 'issues',)
        extra_kwargs = {'password':{'write_only':True}}



