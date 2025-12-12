from .views import(
    CustomerListView,
    CustomerDetailView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    SignUpView,
)
from . import views

from django.urls import path

urlpatterns = [
    # ユーザー登録
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # 顧客一覧ページ
    
    # path("", ...) はプロジェクト側 urls.py から渡されたルートURLを指す
    path("", CustomerListView.as_view(), name="customer_list"),

    # 顧客詳細ページ
    # <int:pk> は URL の一部（顧客ID）を変数として受け取る
    # 例: /customer/1/  ,  /customer/2/
    path("customer/<int:pk>/", CustomerDetailView.as_view(), name="customer_detail"),
    
    # 新規登録ページ
    path("customer/new/", CustomerCreateView.as_view(), name="customer_create"),

    # 編集ページ
    path("customer/<int:pk>/edit/", CustomerUpdateView.as_view(), name="customer_update"),
    
    # 削除ページ
    path("customer/<int:pk>/delete/", CustomerDeleteView.as_view(), name="customer_delete"),  
    
    # Ajaxで商談履歴を追加するURLパターン
    path('customer/add-activity/', views.ajax_add_activity, name='ajax_add_activity'), 
]
