import uuid

def complete_sale_and_log(method='sms'):
    receipt_id = str(uuid.uuid4())
    tree_saver.log_receipt(receipt_id, method)
    send_receipt(receipt_id, method)
