from celery import Celery

celery_app = Celery(
    "origination",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def run_credit_check(loan_id: str, customer_id: str):
    print(f"Running credit check for customer {customer_id}, loan {loan_id}")
    score = 750
    # Simulated credit check for customer = in reality this would call a credit bureau API
    print(f"Credit score for {customer_id}: {score}")
    return {"loan_id": loan_id, "customer_id": customer_id, "score": score}

