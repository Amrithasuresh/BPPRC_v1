from django.urls import path
from database import views

urlpatterns = [
    path('', views.home, name='home'),
    path('database/', views.database, name='database'),
    path('categorize_database_<str:category>',
         views.categorize_database, name='categorize_database'),
    path('search_database/', views.search_database,
         name='search_database'),
    path('search_database/add_cart/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:database_id>/', views.remove_cart, name='remove_cart'
         ),
    path('clear_session_database/', views.clear_session_database, name='clear_session_database'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('download_sequences/', views.download_sequences,
         name='download_sequences'),
    path('clear_session_user_data/', views.clear_session_user_data,
         name='clear_session_user_data'),
    path('user_data_remove/<int:id>/', views.user_data_remove,
         name='user_data_remove'),
    path('user_data/', views.user_data, name='user_data'),
    path('download_data/', views.download_data, name='download_data'),
    path('download_category_<str:category>', views.download_category,
         name='download_category'),
]
