from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.models import Discount
from core.serializers import DiscountSerializer


class DiscountViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet
):

    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    filterset_fields = ['brand', ]
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def list(self, request, *args, **kwargs):
        try:
            code = request.query_params.get('code', None)
            brand_id = int(request.query_params.get('brand', None))
            order_type = request.query_params.get(
                'order_type', None)  # Optional querystring
        except Exception:
            return super().list(request, *args, **kwargs)

        if not code or not brand_id:
            return super().list(request, *args, **kwargs)

        if not order_type:
            is_existed_discount = Discount.objects.filter(
                code=code, brand__pk=brand_id)
        else:
            is_existed_discount = Discount.objects.filter(
                code=code, brand__pk=brand_id, order_type__contains=order_type)

        if len(is_existed_discount) == 0:
            return Response({'detail': 'Code doesn\'t exist'}, status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(is_existed_discount[0])
        return Response(serializer.data)
