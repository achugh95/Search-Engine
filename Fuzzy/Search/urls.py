from django.conf.urls import url
from . import views

urlpatterns = [

    # One time operation to upload the CSV into the local DB
    url(r'^UpdateDataset$', views.update_dataset, name='update_dataset'),

    # One time operation to delete all the objects of the DB
    url(r'^DeleteDataset$', views.delete_dataset, name='delete_dataset')
]
