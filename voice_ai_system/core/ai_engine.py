from openai import OpenAI
from django.conf import settings
from .models import Customer, Loan, ConversationLog

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_last_stage(customer):
    last_log = ConversationLog.objects.filter(customer=customer).order_by('-timestamp').first()
    return last_log.stage if last_log else "START"


def generate_ai_response(customer, loan, user_message, stage):
    prompt = f"""
You are a professional loan collection agent.

Customer Name: {customer.name}
Loan Amount: {loan.amount}
Due Date: {loan.due_date}
Current Stage: {stage}

User said: "{user_message}"

Respond professionally, politely, and guide the user towards repayment.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a banking assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    # except Exception as e:
    #     print("OpenAI Error:", e)
    #     return "Sorry, I am facing some issues right now. Please try again later."
    except Exception as e:
        # print("🔥 OpenAI Error:", str(e))
        # return "Error occurred"
        if "quota" in str(e).lower():
            return "Our system is temporarily unavailable. Please try again later."
    

   
def generate_response(phone, user_message):
    if not user_message:
        return "Message cannot be empty"

    try:
        customer = Customer.objects.get(phone=phone)
        loan = Loan.objects.get(customer=customer)
    except Customer.DoesNotExist:
        return "Customer not found"

    stage = get_last_stage(customer)

    response = generate_ai_response(customer, loan, user_message, stage)

    ConversationLog.objects.create(
        customer=customer,
        message=user_message,
        sender="USER",
        stage=stage
    )

    ConversationLog.objects.create(
        customer=customer,
        message=response,
        sender="AI",
        stage=stage
    )

    return response