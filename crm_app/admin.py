from django.contrib import admin
from .models import Customer, Tag, Activity

# Register your models here.

# Adminサイトでのモデルを登録
"""
admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Activity)
"""

# CustomerモデルのAdmin設定
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    
# CustomerモデルのAdmin設定
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # 一覧画面を見やすくするためにnameフィールドを表示
    list_display = ('company_name', 'contact_name', 'email', 'user', 'created_at', 'updated_at')
    #絞り込み用のフィルターを追加
    list_filter = ('user', 'tags', 'created_at')
    # 検索機能を追加
    search_fields = ('company_name', 'contact_name', 'email')
    # 編集画面での表示順序を指定
    fieldsets = (
        ('基本情報',{'fields':('company_name', 'contact_name', 'email', 'phone')}),
        ('担当・タグ',{'fields':('user', 'tags')}),
    )
    # 多対多(tags)を編集しやすくなる
    filter_horizontal = ('tags',)
    # 編集画面で自動入力される項目を読み取り専用にする
    readonly_fields = ('created_at', 'updated_at')
    
# ActivityモデルのAdmin設定
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    # 一覧画面を見やすくするためにcompany_name, status, activity_dateフィールドを表示
    list_display = ('customer', 'activity_date', 'status', 'created_at', 'updated_at')
    # 絞り込み用のフィルターを追加
    list_filter = ('status', 'activity_date', 'customer__user')
    # 検索機能を追加
    search_fields = ('customer__company_name', 'note')
    # 編集画面での表示順序を指定
    fields = ('customer', 'activity_date', 'status', 'note')
    # 編集画面で自動入力される項目を読み取り専用にする
    raw_id_fields = ('customer',)