from django.core.exceptions import ValidationError

from rest_framework.decorators import list_route
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from ..v0.serializers import UsageStatsSerializer

from apps.plea.models import CourtEmailCount, UsageStats


class PublicStatsViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def render_api_error(self, message):
        error = {
            "error": message
        }

        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        start_date = request.GET.get("start", None)
        end_date = request.GET.get("end", None)

        try:
            stats = CourtEmailCount.objects.get_stats(start=start_date, end=end_date)
        except ValidationError as e:
            return self.render_api_error("; ".join(e.messages))

        return Response(stats)

    @list_route()
    def days_from_hearing(self, request):
        stats = CourtEmailCount.objects.get_stats_days_from_hearing()

        return Response(stats)

    @list_route()
    def by_week(self, request):

        stats = UsageStats.objects.last_six_months()

        serializer = UsageStatsSerializer(stats, many=True)

        return Response(serializer.data)

    @list_route()
    def by_court(self, request):
        start_date = request.GET.get("start", None)
        end_date = request.GET.get("end", None)

        try:
            stats = CourtEmailCount.objects.get_stats_by_court(start=start_date, end=end_date)
        except ValidationError as e:
            return self.render_api_error("; ".join(e.messages))

        return Response(stats)
