import uuid

def generate_transaction_id():
    transaction_id = str(uuid.uuid4())
    return f"TXN-{transaction_id[:8]}"