""" Declear class-based view for exposing MenuItem model """

import datetime

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.models import Brand, TimeSlot
from core.serializers import TimeSlotSerializer


class TimeSlotView(APIView):
    """ Viewset that represent the MenuItem with signature_dish flag """
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        return TimeSlot.objects.all()

    def get(self, request):
        """ GET function to return list timeslot """
        brand_id = self.request.query_params.get('brand', None)
        date = self.request.query_params.get('date', None)
        days = self.request.query_params.get('days', None)

        if not brand_id:
            return Response({'detail': 'Brand should be specified'}, status.HTTP_400_BAD_REQUEST)

        if not date and not days:
            return Response(
                {'detail': 'Should provide specific times or time range'},
                status.HTTP_400_BAD_REQUEST,
            )

        if date and days:
            return Response(
                {'detail': 'Should provide only specific times or time range, not both'},
                status.HTTP_400_BAD_REQUEST,
            )

        # Convert and verify the input.
        brand = get_object_or_404(Brand, pk=brand_id)
        date_list = []

        if date:
            try:
                date_list = [
                    datetime.datetime.strptime(date, '%d-%m')
                    .date()
                    .replace(year=datetime.datetime.now().year)
                ]
            except ValueError:
                return Response(
                    {'detail': 'Date is invalid'},
                    status.HTTP_400_BAD_REQUEST,
                )
        else:
            try:
                days = int(days)
                if days <= 0:
                    raise ValueError
            except ValueError:
                return Response(
                    {'detail': 'Days is invalid'},
                    status.HTTP_400_BAD_REQUEST,
                )

            today = datetime.datetime.today()
            for x in range(0, days):
                date_list.append((today + datetime.timedelta(days=x)).date())

        # Generate result
        serializer = TimeSlotSerializer(
            {"brand": brand, "date_list": date_list})

        return Response({
            "results": serializer.data
        }, status.HTTP_200_OK)
