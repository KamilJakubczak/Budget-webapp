from django.urls import include, path
from . import views

urlpatterns = [
    # path('', views.EntryListView.as_view(), name='entry_changelist'),
    # path('add/', views.EntryCreateView.as_view(), name='entry_add'),
    path('add2/',views.add2, name='add2'),
    path('new_entry/', views.new_entry, name = 'new_entry'),
    # path('<int:pk>/', views.EntryUpdateView.as_view(), name='entry_change'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-types/', views.load_types, name='ajax_load_types'),
    path('ajax/load-payments/', views.load_payments, name='ajax_load_payments'),
    path('',views.full_list, name='view_all'),
    path('view/<int:year>/<int:month>', views.view_month, name ='view_month'),
    path('savings/', views.savings_graph, name='savings'),
    path('<int:entry_id>/del_entry', views.del_entry, name='del_entry'),
    path('transactions',views.show_transactions, name='transactions')
]

