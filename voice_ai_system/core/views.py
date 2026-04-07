from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Loan, ConversationLog
from .serializers import CustomerSerializer, LoanSerializer, ConversationLogSerializer



# 1. Get Customer Details
@api_view(['GET'])
def get_customer(request, phone):
    try:
        customer = Customer.objects.get(phone=phone)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)


# 2. Get Loan Details
@api_view(['GET'])
def get_loan(request, phone):
    try:
        customer = Customer.objects.get(phone=phone)
        loan = Loan.objects.get(customer=customer)
        serializer = LoanSerializer(loan)
        return Response(serializer.data)
    except:
        return Response({"error": "Loan not found"}, status=404)


# 3. Add Conversation Log
@api_view(['POST'])
def add_log(request):
    serializer = ConversationLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Log saved"})
    return Response(serializer.errors, status=400)


# 4. Update Loan Status
@api_view(['POST'])
def update_loan(request, phone):
    try:
        customer = Customer.objects.get(phone=phone)
        loan = Loan.objects.get(customer=customer)
        
        status = request.data.get('status')
        loan.status = status
        loan.save()

        return Response({"message": "Loan updated"})
    except:
        return Response({"error": "Something went wrong"}, status=400)
    

from .ai_engine import generate_response


@api_view(['POST'])
def chat_with_ai(request, phone):
    message = request.data.get('message')

    if not message:
        return Response({"error": "Message required"}, status=400)

    response = generate_response(phone, message)

    return Response({"response": response})




def dashboard(request):
    total_customers = Customer.objects.count()
    total_loans = Loan.objects.count()
    total_logs = ConversationLog.objects.count()

    paid_loans = Loan.objects.filter(status='PAID').count()
    pending_loans = Loan.objects.filter(status='PENDING').count()

    recent_logs = ConversationLog.objects.order_by('-timestamp')[:10]

    context = {
        'total_customers': total_customers,
        'total_loans': total_loans,
        'total_logs': total_logs,
        'paid_loans': paid_loans,
        'pending_loans': pending_loans,
        'recent_logs': recent_logs
    }

    return render(request, 'dashboard.html', context)