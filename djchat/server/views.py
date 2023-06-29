from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if by_user or by_serverid and not request.user.is_authenticated:
            raise AuthenticationFailed(detail="User must be authenticated")

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            self.queryset = self.queryset.filter(member__id=request.user.id)

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset:
                    raise ValidationError(
                        detail=f"Server with id {by_serverid} not found"
                    )
            except ValueError:
                raise ValidationError(
                    detail=f"Invalid value for serverid: {by_serverid}"
                )

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
