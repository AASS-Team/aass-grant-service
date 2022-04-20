from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from grants.models import Grant


class GrantsList(APIView):
    """
    List all grants, or create a new grant.
    """

    serializer_class = serializers.GrantSerializer

    def get(self, request, format=None):
        grants = Grant.objects.all()
        serializer = self.serializer_class(grants, many=True)

        return Response(data=serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                    "message": "Nepodarilo sa uložiť grant",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            data={
                "message": "Grant uložený",
            },
            status=status.HTTP_201_CREATED,
        )


class GrantDetail(APIView):
    """
    Retrieve, update or delete a lab instance.
    """

    def get_object(self, id):
        try:
            return Grant.objects.get(pk=id)
        except Grant.DoesNotExist:
            raise NotFound()

    def get(self, request, id, format=None):
        grant = self.get_object(id)
        serializer = serializers.GrantSerializer(grant)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        grant = self.get_object(id)
        serializer = serializers.GrantSerializer(grant, data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "message": "Nepodarilo sa uložiť grant",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(data={"message": "Grant uložený"})

    def delete(self, request, id, format=None):
        grant = self.get_object(id)
        grant.delete()

        return Response(
            data={
                "message": "Grant vymazaný",
            },
        )
