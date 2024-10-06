class Request():
    def __init__(self, id, user_id, config_id, status, req_msg_for_admin, receipt_image, chat_id):
        self.id = id,
        self.user_id = user_id
        self.config_id = config_id
        self.status = status
        self.req_msg_for_admin = req_msg_for_admin
        self.receipt_image = receipt_image
        self.chat_id = chat_id
