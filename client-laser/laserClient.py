import socketio
import asyncio
import signal

from Laser import Laser

sio = socketio.AsyncClient()
laser = Laser()

@sio.event
async def connect():
    print('Connected to server')

@sio.event
async def connect_error(data):
    print('Connection failed')

@sio.event
async def disconnect(reason):
    if reason == sio.reason.CLIENT_DISCONNECT:
        print('the client disconnected')
    elif reason == sio.reason.SERVER_DISCONNECT:
        print('the server disconnected the client')
    else:
        print('disconnect reason:', reason)

@sio.event
async def hello():
    print('Server said hello')

@sio.event
async def key_press(data):
    print('Received key_press event: ', data)
    laser.handle_key_press(data['key'])
    return 'OK'

@sio.on('*')
async def unhandled(event, sid, data):
    print('Unhandled event: ' ,event, sid,data)

async def main():
    signal.signal(signal.SIGINT, shutdown_handler)

    await sio.connect('http://192.168.0.127:50002')
    print('My sid is ', sio.sid)
    await sio.emit('i_am_laser')
    await sio.wait()

def shutdown_handler(signum, frame):
    print('Got CTRL+C')
    laser.teardown()
    exit (0)

if __name__ == "__main__":
    asyncio.run(main())