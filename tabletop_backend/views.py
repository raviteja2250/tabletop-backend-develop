""" tabletop_backend/views.py """
from django.http import JsonResponse


def health_check_view(request):
    """ Function for the healthcheck endpoint """
    return JsonResponse({'detail': 'OK'}, status=200)
