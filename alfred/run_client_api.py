import argparse

import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel

from alfred.client import Client
from alfred.client.ssh.sshtunnel import SSHTunnel

alfred_app = FastAPI()

global client
global webhook_port

server_connected = False

ALFRED_META_CONFIG = {
    'model': '',
    'model_type': '',
    'end_point': '',
    'end_point_port': '',
    'username': '',
    'final_host': '',
}


class ALFRED_CONFIG(BaseModel):
    model: str
    model_type: str
    end_point: str
    end_point_port: str
    username: str
    final_host: str


@alfred_app.get("/")
async def root():
    return {"message": "This is Alfred! Hello World!"}


@alfred_app.get("/status")
async def status():
    return {"status": "ok"}


###########################################################
@alfred_app.get("/alfred_server/port")
async def get_alfred_server_port():
    return {'port': ALFRED_META_CONFIG['end_point_port']}


@alfred_app.get("/alfred_server/model")
async def get_alfred_server_model():
    return {'model': ALFRED_META_CONFIG['model']}


@alfred_app.get("/alfred_server/model_type")
async def get_alfred_server_model_type():
    return {'model_type': ALFRED_META_CONFIG['model_type']}


@alfred_app.get("/alfred_server/end_point")
async def get_alfred_server_end_point():
    return {'end_point': ALFRED_META_CONFIG['end_point']}


@alfred_app.get("/alfred_server/username")
async def get_alfred_server_username():
    return {'username': ALFRED_META_CONFIG['username']}


@alfred_app.get("/alfred_server/final_host")
async def get_alfred_server_final_host():
    return {'final_host': ALFRED_META_CONFIG['final_host']}


@alfred_app.get("/alfred_server/webhook_port")
async def get_alfred_server_webhook_port():
    return {'webhook_port': str(webhook_port)}


@alfred_app.get("/alfred_server/connected")
async def set_alfred_server_connected():
    return {'connected': str(server_connected).lower()}


###########################################################
# setters
@alfred_app.post("/alfred_server/port")
async def set_alfred_server_port(request: Request):
    request = await request.json()
    ALFRED_META_CONFIG['end_point_port'] = request.json()['port']
    return {'port': ALFRED_META_CONFIG['end_point_port']}


@alfred_app.post("/alfred_server/model")
async def set_alfred_server_model(request: Request):
    request = await request.json()
    ALFRED_META_CONFIG['model'] = request.json()['model']
    return {'model': ALFRED_META_CONFIG['model']}


@alfred_app.post("/alfred_server/model_type")
async def set_alfred_server_model_type(request: Request):
    request = await request.json()
    ALFRED_META_CONFIG['model_type'] = request.json()['model_type']
    return {'model_type': ALFRED_META_CONFIG['model_type']}


@alfred_app.post("/alfred_server/end_point")
async def set_alfred_server_end_point(request: Request):
    request = await request.json()
    ALFRED_META_CONFIG['end_point'] = request.json()['end_point']
    return {'end_point': ALFRED_META_CONFIG['end_point']}


@alfred_app.post("/alfred_server/username")
async def set_alfred_server_username(request: Request):
    request = await request.json()
    ALFRED_META_CONFIG['username'] = request.json()['username']
    return {'username': ALFRED_META_CONFIG['username']}


@alfred_app.post("/alfred_server/final_host")
async def set_alfred_server_final_host(request: Request):
    request = await request.json()
    ALFRED_META_CONFIG['final_host'] = request.json()['final_host']
    return {'final_host': ALFRED_META_CONFIG['final_host']}


@alfred_app.post("/alfred_server/webhook_port")
async def set_alfred_server_webhook_port(request: Request):
    global webhook_port
    request = await request.json()
    webhook_port = int(request['port'])
    print(f'webhook_port: {webhook_port}')
    return {'webhook_port': str(webhook_port)}


###########################################################
# Connection Handshakes


@alfred_app.post("/alfred_server/endpoint_cfg")
async def set_alfred_server_endpoint_cfg(data: ALFRED_CONFIG):
    def connect_to_server():
        global client
        global webhook_port
        global server_connected

        def api_handler(title, instructions, prompt_list):
            # This handler will analyze the prompt and prompt fastapi for the user input from the front end
            # first post the title and instructions
            # then iterate and post the prompt_list to get user inputs
            # return the user inputs
            global webhook_port

            print(title)
            print(instructions)
            user_input = []
            for (prompt, echo) in prompt_list:
                # send request to the flutter app
                # change api field
                res = requests.post(f'http://localhost:{webhook_port}',
                                    json={
                                        'prompt': prompt,
                                        'echo': echo
                                    }).text
                user_input.append(res)
            return user_input

        print("Connecting to server")
        print(ALFRED_META_CONFIG)
        # Setup SSH Tunnel
        for i in range(0, 5):
            try:
                print("Setting up SSH tunnel, Trying {} ...".format(i))
                ssh_tunnel = SSHTunnel(
                    remote_host=ALFRED_META_CONFIG['end_point'],
                    remote_port=ALFRED_META_CONFIG['end_point_port'],
                    username=ALFRED_META_CONFIG['username'],
                    remote_node_address=ALFRED_META_CONFIG['final_host']
                    if len(ALFRED_META_CONFIG['final_host']) > 0 else None,
                    handler=api_handler)
                ssh_tunnel.start()
            except Exception as e:
                print(e)
                print("Authentication failed")
                continue
            break

        print("SSH Tunnel setup at port {}".format(ssh_tunnel.local_port))
        # Setup Client
        client = Client(end_point=f"127.0.0.1:{ssh_tunnel.local_port}", )
        print("Client setup")
        server_connected = True
        print("Server connected")

    ALFRED_META_CONFIG['model'] = data.model
    ALFRED_META_CONFIG['model_type'] = data.model_type
    ALFRED_META_CONFIG['end_point'] = data.end_point
    ALFRED_META_CONFIG['end_point_port'] = data.end_point_port
    ALFRED_META_CONFIG['username'] = data.username
    ALFRED_META_CONFIG['final_host'] = data.final_host

    connect_to_server()

    return ALFRED_META_CONFIG


###########################################################


@alfred_app.post("/alfred_server/completion")
async def alfred_server_completion(request: Request):
    request = await request.json()
    prompt = request['prompt']
    if client:
        res = client(prompt).prediction
        return {'completion': res}
    else:
        return {'completion': 'Error: No alfred client connected!'}


###########################################################
@alfred_app.get("/alfred_server/cache")
async def set_alfred_server_connected():
    import pandas as pd
    import numpy as np
    from pretty_html_table import build_table

    df = pd.DataFrame(np.arange(9).reshape(3, 3), list('ABC'), list('XYZ'))
    html_table_blue_light = build_table(df, 'blue_light')
    return {'html': html_table_blue_light}


###########################################################
def main(args):
    import uvicorn

    uvicorn.run(
        alfred_app,
        host="0.0.0.0",
        port=int(args.port),
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9719)
    main(parser.parse_args())
