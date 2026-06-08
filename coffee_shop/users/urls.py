app_name = "users"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path("password_reset_done/", views.password_reset_done, name="password_reset_done"),
    path(
        "password_reset_confirm/<str:uidb64>/<str:token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        views.password_reset_complete,
        name="password_reset_complete",
    ),
]
