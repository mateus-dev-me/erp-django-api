from django.urls import include, path

urlpatterns = [
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/companies/', include('companies.urls')),
]
