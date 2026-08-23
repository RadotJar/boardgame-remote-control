import socketio
import uvicorn

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

@sio.event
async def connect( sid, data):
    print('connect ',sid)
    await sio.emit('hello', None, to=sid)

@sio.event
async def disconnect( sid, reason ):
    print('disconnect ', sid, reason)

@sio.event
async def i_am_laser(sid):
    print('Client identified itself as a laser: ', sid)
    await sio.enter_room(room='laser_clients', sid=sid)

@sio.event
async def i_am_web(sid):
    print('Client identified itself as a web client: ', sid)
    await sio.enter_room(room='web_clients',sid=sid)

@sio.event
async def key_press(sid, data):
    print('Received key_press event from ', sid)
    print('Pressed ', data['key'])
    response = await sio.call('key_press', data, to='laser_clients')
    if ( response == 'OK' ):
        print('laser ACKED')
        await sio.call('key_press_ack', data, to='web_clients')

@sio.on('*')
async def unhandled(event, sid, data):
    print('Unhandled event: ', event, sid, data)

if __name__ == '__main__':
    uvicorn.run("server:app", port=5000, log_level='info')