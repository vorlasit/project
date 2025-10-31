from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages 
from .models import Wallet
from .forms import DepositForm, WithdrawForm 
from res.models import CustomUser as User
 
@login_required
def wallet_detail(request):
    """
    Display the logged-in user's wallet balance and transaction history.
    """
    # Get or create wallet for the user
    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    # Get transactions (latest first)
    transactions = wallet.transactions.all().order_by('-created_at')

    context = {
        'wallet': wallet,
        'transactions': transactions,
    }
    return render(request, 'wallet_detail.html', context)

def admin_user_list(request):
    """
    List all users with their wallet balances and actions.
    """
    users = User.objects.all().order_by('username')
    # Preload wallets to reduce queries
    wallets = Wallet.objects.all() 

    context = {
        'users': users,
        'wallet_dict': wallets,
    }
    return render(request, 'admin_user_list.html', context)

@login_required
def deposit(request):
    """Deposit money to user's wallet."""
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            wallet.deposit(amount)
            messages.success(request, f'Deposited {amount} to your wallet.')
            return redirect('wallet_detail')
    else:
        form = DepositForm()
    return render(request, 'wallet_deposit.html', {'form': form})


@login_required
def withdraw(request):
    """Withdraw money from user's wallet."""
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
                wallet.withdraw(amount)
                messages.success(request, f'Withdrew {amount} from your wallet.')
                return redirect('wallet_detail')
            except ValueError:
                messages.error(request, 'Insufficient balance.') 


@user_passes_test(lambda u: u.is_staff)
def admin_deposit_user(request, user_id):
    """Admin deposits money to a specific user's wallet."""
    user = get_object_or_404(User, id=user_id)
    wallet, _ = Wallet.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            wallet.deposit(amount)
            messages.success(request, f'Deposited {amount} to {user.username}\'s wallet.')
            return redirect('user_list')
    else:
        form = DepositForm()
    return render(request, 'admin_user_deposit.html', {'form': form, 'user': user})


@user_passes_test(lambda u: u.is_staff)
def admin_withdraw_user(request, user_id):
    """Admin withdraws money from a specific user's wallet."""
    user = get_object_or_404(User, id=user_id)
    wallet, _ = Wallet.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
                wallet.withdraw(amount)
                messages.success(request, f'Withdrew {amount} from {user.username}\'s wallet.')
                return redirect('admin_user_list')
            except ValueError:
                messages.error(request, f'{user.username} has insufficient balance.')
    else:
        form = WithdrawForm()
    return render(request, 'admin_user_withdraw.html', {'form': form, 'user': user})
