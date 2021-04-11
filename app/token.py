# CPR MP FOR W2OL-PY-R4 2021 A.R.R.
from flask import Flask
from app import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def createToken(userId):
    s = Serializer(app.config["SECRET_KEY"],expires_in=36000)
    token = s.dumps({"id":userId}).decode("ascii")
    return token

def verifyToken(token):
    #参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(app.config["SECRET_KEY"])
    try:
        data = s.loads(token)
    except Exception:
        return None
    return data["id"]

def checkAuth(request):
    if not 'Authorization' in request.headers:
        return None
    current_token = request.headers['Authorization'].split( )[1]
    current_id = verifyToken(current_token)
    if not current_id:
        return None
    return current_id