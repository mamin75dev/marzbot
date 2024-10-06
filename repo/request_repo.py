from models.request_model import Request
from repo.db import db


class RequestRepo:
    def __init__(self):
        pass

    @classmethod
    def insert_request(cls, request: Request):
        query = "INSERT INTO requests (user_id, config_id, status, req_msg_for_admin, receipt_image, chat_id) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (request.user_id, request.config_id, request.status, request.req_msg_for_admin, request.receipt_image, request.chat_id)
        db.insert(query, values)

    @classmethod
    def find_request_by_user_id(cls, user_id):
        data = db.select(f"SELECT * FROM requests WHERE user_id={user_id}")
        return data[-1] if data else None
