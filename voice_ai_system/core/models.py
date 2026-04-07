from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField()
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.customer.name} - {self.amount}"


class ConversationLog(models.Model):

    SENDER_CHOICES = [
    ('AI', 'AI'),
    ('USER', 'User'),

    ]
    
    STAGE_CHOICES = [
    ('START', 'Start'),
    ('REMINDER', 'Reminder'),
    ('NEGOTIATION', 'Negotiation'),
    ('CLOSURE', 'Closure'),
]

    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.CharField(max_length=10 , choices=SENDER_CHOICES)  # 'AI' or 'USER'
    timestamp = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='START')

    def __str__(self):
        return f"{self.customer.name} - {self.sender}"