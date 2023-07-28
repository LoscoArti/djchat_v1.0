from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError

# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Server
from .schema import server_list_docs
from .serializer import CategorySerializer, ServerSerializer


class CategoryListViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()
    # permission_classes = [IsAuthenticated]

    @server_list_docs
    def list(self, request):
        """Returns a list of servers filtered by various parameters.

        This method retrieves a queryset of servers based on the query parameters
        provided in the `request` object. The following query parameters are supported:

        - `category`: Filters servers by category name.
        - `qty`: Limits the number of servers returned.
        - `by_user`: Filters servers by user ID, only returning servers that the user is a member of.
        - `by_serverid`: Filters servers by server ID.
        - `with_num_members`: Annotates each server with the number of members it has.

        Args:
        request: A Django Request object containing query parameters.

        Returns:
        A queryset of servers filtered by the specified parameters.

        Raises:
        AuthenticationFailed: If the query includes the 'by_user' or 'by_serverid'
            parameters and the user is not authenticated.
        ValidationError: If there is an error parsing or validating the query parameters.
            This can occur if the `by_serverid` parameter is not a valid integer, or if the
            server with the specified ID does not exist.

        Examples:
        To retrieve all servers in the 'gaming' category with at least 5 members, you can make
        the following request:

            GET /servers/?category=gaming&with_num_members=true&num_members__gte=5

        To retrieve the first 10 servers that the authenticated user is a member of, you can make
        the following request:

            GET /servers/?by_user=true&qty=10

        """
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        queryset = self.queryset

        if category:
            queryset = queryset.filter(category__name=category)

        if by_user:
            if by_user and request.user.is_authenticated:
                queryset = queryset.filter(member__id=request.user.id)
            else:
                raise AuthenticationFailed()

        if with_num_members:
            queryset = queryset.annotate(num_members=Count("member"))

        if qty:
            queryset = queryset[: int(qty)]

        if by_serverid:
            try:
                queryset = queryset.filter(id=by_serverid)
                if not queryset:
                    raise ValidationError(
                        detail=f"Server with id {by_serverid} not found"
                    )
            except ValueError:
                raise ValidationError(
                    detail=f"Invalid value for serverid: {by_serverid}"
                )

        serializer = ServerSerializer(
            queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
