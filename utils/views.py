"""
    Define abstract classes that are used to interact with drf-view
"""
from django.db.models import Prefetch
from django.core.exceptions import ValidationError

from rest_framework.mixins import CreateModelMixin

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ViewHandlerModeMixin:
    """
        Class to handle the view of object have `number_of_view` field
    """

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a model instance and increase the view
        """
        # Update the number of view when user request to view an post.
        instance = self.get_object()
        instance.number_of_view += 1
        instance.save(update_fields=("number_of_view", ))

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LikeHandlerModeMixin:
    """
        Class to handle the view with like and unlike feature
        Note:
            - Please with the subclass of LikeAndUnLikeSerializer
            or any one has the `like()` and `unlike()` method
    """
    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def like(self, request, *args, **kwargs):
        """ Request to like a post """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        try:
            serializer.like()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as err:
            return Response({'detail': err}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def unlike(self, request, *args, **kwargs):
        """ Request to unlike a post """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        try:
            serializer.unlike()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as err:
            return Response({'detail': err}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list':
            # Only prefetch the `likes` when list objects
            # Because it will cache data and effect the like/unlike
            queryset = queryset.prefetch_related('likes')
            queryset = queryset.prefetch_related(
                Prefetch('likes__user'),
            )

        return queryset


class BulkCreateModeMixin(CreateModelMixin):
    """
        Class to handle the creation for multi-object
    """
    @action(detail=False, methods=['post'])
    def bulk(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
