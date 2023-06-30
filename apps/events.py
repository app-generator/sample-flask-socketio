from flask_socketio import SocketIO, emit

socketio = SocketIO(logger=True)

@socketio.on('connect')
def connect_event():
    print('Client connected')
