from django.conf.urls import url, include


urlpatterns = (
    url(r'^v0/', include('api.v0.urls', namespace="api-v0")),
    url(r'^stats/', include('api.stats.urls', namespace="api-stats")),
)
