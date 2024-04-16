from rest_framework import serializers
from .models import Plan, PlanDepartment


class PlanSerializer(serializers.ModelSerializer):
    month_display = serializers.CharField(source='get_month_display')

    class Meta:
        model = Plan
        fields = ['plan_department', 'month_display', 'plan_integer', 'plan_money']


class PlanDepartmentSerializer(serializers.ModelSerializer):
    data = PlanSerializer(source='plan_set', many=True)

    class Meta:
        model = PlanDepartment
        fields = ['plan_subtype', 'data']
