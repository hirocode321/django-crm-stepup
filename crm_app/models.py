from django.db import models
from django.contrib.auth.models  import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    company_name = models.CharField(max_length=100, verbose_name="会社名")
    contact_name = models.CharField(max_length=50, verbose_name="担当者名")
    email = models.EmailField(max_length=100, unique=True, verbose_name="メールアドレス")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号")
    # Django標準のUserモデルと紐付け
    # 担当者が削除されても顧客情報は残るようにする(SEL NULL)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="営業担当者")
    # Tagモデルとの多対多の関係
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="タグ")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    def __str__(self):
        return f"{self.company_name} # Adminサイトを見やすくするために会社名を表示"

# 商談履歴モデル
class Activity(models.Model):
    # 進捗ステータスの選択肢
    STATUS_CHOICES = (
        ('APPO','アポ'),
        ('MEETING','商談中'),
        ('PROPOSAL','提案中'),
        ('WON','受注'),
        ('LOST','失注'),
    )
    
    #【重要】 （ustomerモデルと1対多で連携)
    # 顧客が削除されたら、関連する商談履歴も一緒に削除する（CASCADE）
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="顧客")
    activity_date = models.DateField(verbose_name="商談日")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="ステータス")
    note = models.TextField(blank=True, null=True, verbose_name="商談メモ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    def __str__(self):
        return f"{self.customer.company_name} - {self.get_status_display()} # Adminサイトを見やすくするために会社名とステータスを表示"