from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.list_media, name='list_all_media'),
    path('add/', views.add_media, name='add_media'),
    path('show/<int:media_id>', views.get_by_id, name='show_media'),
    path('update/<int:media_id>', views.update_media, name='update_media'),
    path('delete/<int:media_id>', views.delete_media, name='delete_media'),

    path('post/', views.ListAddView.as_view(), name='list_post'),
    path('generic/', views.ListAddGenericView.as_view(), name='generics_mixins'),
]
