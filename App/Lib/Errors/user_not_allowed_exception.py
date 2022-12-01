class UserNotAllowedException(Exception):
    def __init__(self, user_id: int):
        self.message = f'User {user_id} not allowed to use bot.'
        super().__init__(self.message)
