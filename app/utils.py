from flask_restful import Resource


class Home(Resource):
    """
    Returns welcome message to new user
    url: /api/v1/
    """
    def get(self):
        return {"message": "Welcome to live-it! To get started, register a new user or login"}
