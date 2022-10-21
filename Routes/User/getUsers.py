from init import db, app
from Schema.init import users_schema
from Models.Session import Session
from Models.User import User
from flask import request, jsonify, Response
import time

@app.route('/user', methods=['GET'])
def get_users():
    # Require Authorization header
    try:
        access_token = request.headers['Authorization']
    except:
        return Response(status=401)
    session = Session.query.filter_by(access_token=access_token).first()
    # Return 401 if accesss token is expired or does not belong to an admin account
    if session.user.admin == False or time.time() > session.access_expiration:
        return Response(status=401)

    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)