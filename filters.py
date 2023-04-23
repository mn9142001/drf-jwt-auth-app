import django_filters 
from django.contrib.auth.models import User

class UserMailFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['email']
