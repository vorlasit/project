# bank/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from decimal import Decimal

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balance(request):
    account = request.user.account
    serializer = AccountSerializer(account)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    account = request.user.account
    amount = Decimal(request.data.get('amount', 0))
    account.balance += amount
    account.save()
    Transaction.objects.create(receiver=account, amount=amount, type='deposit')
    return Response({'message': 'Deposit successful', 'balance': account.balance})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    account = request.user.account
    amount = Decimal(request.data.get('amount', 0))
    if account.balance < amount:
        return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
    account.balance -= amount
    account.save()
    Transaction.objects.create(sender=account, amount=amount, type='withdraw')
    return Response({'message': 'Withdraw successful', 'balance': account.balance})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request):
    sender = request.user.account
    receiver_number = request.data.get('receiver_account')
    amount = Decimal(request.data.get('amount', 0))
    reference = request.data.get('reference', '')

    try:
        receiver = Account.objects.get(account_number=receiver_number)
    except Account.DoesNotExist:
        return Response({'error': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)

    if sender.balance < amount:
        return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

    # Update balances
    sender.balance -= amount
    receiver.balance += amount
    sender.save()
    receiver.save()

    # Record transaction
    Transaction.objects.create(
        sender=sender,
        receiver=receiver,
        amount=amount,
        type='transfer',
        reference=reference
    )

    return Response({'message': 'Transfer successful', 'balance': sender.balance})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_order(request):
    """ ใช้เมื่อจ่ายเงิน order ในระบบ ecommerce """
    account = request.user.account
    amount = Decimal(request.data.get('amount', 0))
    order_id = request.data.get('order_id', '')

    if account.balance < amount:
        return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

    account.balance -= amount
    account.save()

    Transaction.objects.create(
        sender=account,
        amount=amount,
        type='payment',
        reference=f"Order #{order_id}"
    )

    return Response({'message': f'Payment for Order {order_id} successful', 'balance': account.balance})
