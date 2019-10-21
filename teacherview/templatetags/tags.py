from django import template
from django.contrib.auth.models import User

register= template.Library()

@register.simple_tag
def teacher_name(request):
    teach_id = request.COOKIES.get('id')
    user = User.objects.get(pk=int(teach_id))

    return user.first_name + " " + user.last_name