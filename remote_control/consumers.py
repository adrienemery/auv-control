from channels import Group, Channel
from auv.models import AUVData, AUV


def ws_add(message):
    """Connected to websocket.connect"""
    # add anyone who connects to the same group so which
    # acts as a passthrough for both connected clients
    # ie. a chat room
    Group("remote_control").add(message.reply_channel)


def ws_message(message):
    """# Connected to websocket.receive"""
    # TODO define message format between client and AUV
    Group("remote_control").send({
        "text": "[user] %s" % message.content['text'],
    })


def ws_disconnect(message):
    """Connected to websocket.disconnect"""
    Group("remote_control").discard(message.reply_channel)


def log_data(message):
    """Log data sent from AUV"""
    address = message.get('address')
    auv = AUV.objects.get(address=address)
    data = message.get('data')
    AUVData.log(auv, **data)
