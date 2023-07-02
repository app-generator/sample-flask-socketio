from flask_socketio import SocketIO, emit

socketio = SocketIO(cors_allowed_origins='*', logger=True)

@socketio.on('connect')
def connect_event():
    print('Client connected')

@socketio.on('message')
def handle_message(data):
    print('This is a message:', data)

@socketio.on('new event')
def handle_new_event(data):
    print('A new event was emitted from the client containing the following payload', data)
    emit('server event', {'data': 'This is how you trigger a custom event from the server side'})

# @socketio.on('sales')
# def handle_sales_save(data):
#     emit('sales', data, broadcase=True)
