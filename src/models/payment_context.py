"""
Payment context data model for the payment reminder agent.
"""
from typing import Optional


class PaymentContext:
    """Data class to hold payment context information"""
    
    def __init__(self, 
                 customer_name: Optional[str] = None,
                 invoice_number: Optional[str] = None,
                 amount_due: Optional[float] = None,
                 due_date: Optional[str] = None,
                 company_name: Optional[str] = None):
        self.customer_name = customer_name or "valued customer"
        self.invoice_number = invoice_number or "your invoice"
        self.amount_due = amount_due
        self.due_date = due_date or "as soon as possible"
        self.company_name = company_name or "our company"
    
    def __repr__(self) -> str:
        return (f"PaymentContext(customer_name='{self.customer_name}', "
                f"invoice_number='{self.invoice_number}', "
                f"amount_due={self.amount_due}, "
                f"due_date='{self.due_date}', "
                f"company_name='{self.company_name}')")