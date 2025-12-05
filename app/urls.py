from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from app.views import (
    main, newsletter, usage
)
from app.api import (
    drug, provider, order
)

urlpatterns = [
    # login
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(
        template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(
        template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # files
    re_path(r'^files/(?P<path>.*)$', main.get_file),

    # drug
    path('drug-list', drug.DrugListView.as_view()),
    path('drug-list-by-title', drug.DrugListByTitleView.as_view()),
    path('drug-list-by-provider', drug.DrugListByProviderView.as_view()),
    path('drug-by-id', drug.DrugInfoView.as_view()),

    # provider
    path('provider-by-name', provider.ProviderByName.as_view()),
    path('provider-username', provider.ProviderTgUsernameByName.as_view()),
    path('provider-list', provider.ProviderList.as_view()),

    # order
    path('can-order-for-free', order.CanOrderForFree.as_view()),
    path('order-create', order.CreateOrder.as_view()),

    # newsletter
    path('order-newsletter', newsletter.OrderNewsletterView.as_view()),

    path('usage-rate', usage.usage_rate, name='usage_rate'),


]
