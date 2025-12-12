from django.views.generic import ListView, DetailView
from .models import Customer
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CustomerForm
from django.urls import reverse_lazy
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import ActivityForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# ユーザー登録ビュー
class SignUpView(CreateView):
    """ユーザー登録フォーム"""
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class CustomerCreateView(LoginRequiredMixin, CreateView):
    # 1. どのモデルのデータを取得するか
    model = Customer
    # 2. どのフォームクラスを使うか
    form_class = CustomerForm

    template_name = 'crm_app/customer_form.html'
    success_url = reverse_lazy('customer_list')

    # このメソッドをオーバーライドして、ログインユーザーに紐づく顧客のみを表示
    def form_valid(self, form):
        form.instance.user = self.request.user
        
        # ここでフォームのバリデーションが成功した後の処理を追加できます
        return super().form_valid(form)


# 顧客一覧ページ用のビュー
class CustomerListView(LoginRequiredMixin, ListView):
    """
    顧客一覧を表示するビュー（ListViewを継承）
    """
    # 1. どのモデルのデータを取得するか
    model = Customer
    # 2. どのテンプレートファイルを使うか
    template_name = 'crm_app/customer_list.html'
    # 3. テンプレート内で使う変数名（指定しない場合は object_list）
    context_object_name = 'customers'
    # おまけ：1ページに表示する件数（ページネーション）
    paginate_by = 10
    # おまけ：並び順（会社名順）
    #queryset = Customer.objects.all().order_by('company_name')

    # このメソッドをオーバーライドして、ログインユーザーに紐づく顧客のみを表示
    def get_queryset(self):
        queryset = Customer.objects.filter(user=self.request.user).prefetch_related('tags').order_by('company_name')
        # 検索機能の実装
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(company_name__icontains=query) |
                Q(contact_name__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context
        #return Customer.objects.filter(user=self.request.user).order_by('company_name')

# 顧客詳細ページ用のビュー
class CustomerDetailView(LoginRequiredMixin, DetailView):
    """
    顧客詳細を表示するビュー（DetailViewを継承）
    """
    # 1. どのモデルのデータを取得するか
    model = Customer
    # 2. どのテンプレートファイルを使うか
    template_name = 'crm_app/customer_detail.html'
    # 3. テンプレート内で使う変数名（指定しない場合 object または customer）
    context_object_name = 'customer'

    # このメソッドをオーバーライドして、ログインユーザーに紐づく顧客のみを表示
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user).prefetch_related('tags', 'activity_set')

    
class CustomerUpdateView(LoginRequiredMixin, UpdateView):

    model = Customer
    form_class = CustomerForm
    template_name = 'crm_app/customer_edit.html'
    success_url = reverse_lazy('customer_list')

    # このメソッドをオーバーライドして、ログインユーザーに紐づく顧客のみを表示
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)
    
    
class CustomerDeleteView(LoginRequiredMixin, DeleteView):

    # 1. どのモデルのデータを取得するか 
    model = Customer
    # 2. どのテンプレートファイルを使うか
    template_name = 'crm_app/customer_confirm_delete.html'
    # 3. 削除成功後のリダイレクト先URL
    success_url = reverse_lazy('customer_list')
    # このメソッドをオーバーライドして、ログインユーザーに紐づく顧客のみを表示
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user).prefetch_related('tags')
    
# Ajaxで商談履歴を追加するビュー
@login_required
@require_POST
def ajax_add_activity(request):
    customer_id = request.POST.get('customer_id')
    customer = get_object_or_404(Customer, id=customer_id)
    
    # 自分の担当顧客でなければエラー
    if customer.user != request.user:
        return JsonResponse({'message': 'けんげんがありません'}, status=403)
    
    # フォームを使ってバリデーション
    form = ActivityForm(request.POST)
    
    if form.is_valid():
        activity = form.save(commit=False)
        activity.customer = customer
        activity.save()
        
        # Javascriptに返すデータを作成
        response_data = {
            'message': '商談履歴が追加されました',
            'activity_date': activity.activity_date.strftime('%Y-%m-%d'),
            'status': activity.get_status_display(),
            'note': activity.note,
            }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'message': '入力内容に誤りがあります'}, status=400)