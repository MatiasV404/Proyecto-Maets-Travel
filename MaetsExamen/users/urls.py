from django.urls import path
from django.contrib import admin
from .views import (home, profile, RegisterView,
                    crud_generos, generosAdd, generos_del, generos_edit,
                    listar_lugares, detalles_lugar, donde_ir, TemporadasAPI
                    , create, add_equipment, delete, edit, update, index, guardar_formulario,
                    LugarVisitaAdminView, LugarVisitaCreateView, LugarVisitaUpdateView, LugarVisitaDeleteView,
                    persona_admin, persona_add, persona_edit, persona_delete, crud, donate, payment_done, payment_cancelled, donation_list)
                   

urlpatterns = [
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('', home, name="home"),
    path('donde_ir/', donde_ir, name="donde_ir"),
    path('admin/', admin.site.urls),
    path('crud_generos/', crud_generos, name='crud_generos'),
    path('generosAdd/', generosAdd, name='generosAdd'),
    path('generos_del/<str:pk>/',generos_del, name='generos_del'),
    path('generos_edit/<str:pk>/', generos_edit, name='generos_edit'),
    path('contratar-detalle/', listar_lugares, name='listar_lugares'),
    path('api/lugares/<int:lugar_id>/temporadas/', TemporadasAPI.as_view(), name='api-temporadas'),
    path('contratar-detalle/<int:pk>/', detalles_lugar, name='detalles_lugar'),
    path('create/', create, name='create' ),
    path('add_equipment/', add_equipment, name='add_equipment' ),
    path('delete/<id>/', delete, name='delete' ),
    path('edit/<id>/', edit, name='edit' ),
    path('index/', index, name='index' ),
    path('update/<id>/', update, name='update' ),
    path('guardar/', guardar_formulario, name='guardar_formulario'),
    path('crud/lugarvisita/', LugarVisitaAdminView, name='lugarvisita_admin'),
    path('crud/lugarvisita/add/',LugarVisitaCreateView, name='lugarvisita_add'),
    path('crud/lugarvisita/<int:pk>/edit/', LugarVisitaUpdateView, name='lugarvisita_edit'),
    path('crud/lugarvisita/<int:pk>/delete/', LugarVisitaDeleteView, name='lugarvisita_delete'),
    path('crud/persona/', persona_admin, name='persona_admin'),
    path('crud/persona/add/', persona_add, name='persona_add'),
    path('crud/persona/edit/<int:pk>/', persona_edit, name='persona_edit'),
    path('crud/persona/delete/<int:pk>/', persona_delete, name='persona_delete'),
    path('crud/', crud, name='crud'),
    path('donate/', donate, name='donate'),
    path('payment/done/', payment_done, name='payment_done'),
    path('payment/cancelled/', payment_cancelled, name='payment_cancelled'),
    path('donations/', donation_list, name='donation_list'),   
]
