import socketio
import uvicorn

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)

@sio.event
async def connect( sid, data):
    print('connect ',sid)
    sio.emit('hello', None, to=sid)

@sio.event
async def disconnect( sid, reason ):
    print('disconnect ', sid, reason)

@sio.on('*')
async def unhandled(event, sid, data):
    print('Unhandled event: ', event, sid, data)

if __name__ == '__main__':
    uvicorn.run("server:app", port=5000, log_level='info')