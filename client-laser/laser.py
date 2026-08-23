import socketio
import asyncio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('Connected to server')

@sio.event
async def connect_error(data):
    print('Connectio failed')

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

@sio.on('*')
async def unhandled(event, sid, data):
    print('Unhandled event: ' ,event, sid,data)

async def main():
    data = {}
    await sio.connect('http://localhost:5000', data)
    print('My sid is ', sio.sid)
    await sio.wait()

if __name__ == "__main__":
    asyncio.run(main())