# Run Client Api

[alfred Index](../README.md#alfred-index) /
[Alfred](./index.md#alfred) /
Run Client Api

> Auto-generated documentation for [alfred.run_client_api](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py) module.

## ALFRED_CONFIG

[Show source in run_client_api.py:27](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L27)

#### Signature

```python
class ALFRED_CONFIG(BaseModel):
    ...
```



## alfred_server_completion

[Show source in run_client_api.py:215](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L215)

#### Signature

```python
@alfred_app.post("/alfred_server/completion")
async def alfred_server_completion(request: Request):
    ...
```



## get_alfred_server_end_point

[Show source in run_client_api.py:62](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L62)

#### Signature

```python
@alfred_app.get("/alfred_server/end_point")
async def get_alfred_server_end_point():
    ...
```



## get_alfred_server_final_host

[Show source in run_client_api.py:72](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L72)

#### Signature

```python
@alfred_app.get("/alfred_server/final_host")
async def get_alfred_server_final_host():
    ...
```



## get_alfred_server_model

[Show source in run_client_api.py:52](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L52)

#### Signature

```python
@alfred_app.get("/alfred_server/model")
async def get_alfred_server_model():
    ...
```



## get_alfred_server_model_type

[Show source in run_client_api.py:57](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L57)

#### Signature

```python
@alfred_app.get("/alfred_server/model_type")
async def get_alfred_server_model_type():
    ...
```



## get_alfred_server_port

[Show source in run_client_api.py:47](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L47)

#### Signature

```python
@alfred_app.get("/alfred_server/port")
async def get_alfred_server_port():
    ...
```



## get_alfred_server_username

[Show source in run_client_api.py:67](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L67)

#### Signature

```python
@alfred_app.get("/alfred_server/username")
async def get_alfred_server_username():
    ...
```



## get_alfred_server_webhook_port

[Show source in run_client_api.py:77](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L77)

#### Signature

```python
@alfred_app.get("/alfred_server/webhook_port")
async def get_alfred_server_webhook_port():
    ...
```



## main

[Show source in run_client_api.py:240](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L240)

#### Signature

```python
def main(args):
    ...
```



## root

[Show source in run_client_api.py:36](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L36)

#### Signature

```python
@alfred_app.get("/")
async def root():
    ...
```



## set_alfred_server_connected

[Show source in run_client_api.py:82](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L82)

#### Signature

```python
@alfred_app.get("/alfred_server/connected")
async def set_alfred_server_connected():
    ...
```



## set_alfred_server_connected

[Show source in run_client_api.py:227](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L227)

#### Signature

```python
@alfred_app.get("/alfred_server/cache")
async def set_alfred_server_connected():
    ...
```



## set_alfred_server_end_point

[Show source in run_client_api.py:110](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L110)

#### Signature

```python
@alfred_app.post("/alfred_server/end_point")
async def set_alfred_server_end_point(request: Request):
    ...
```



## set_alfred_server_endpoint_cfg

[Show source in run_client_api.py:143](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L143)

#### Signature

```python
@alfred_app.post("/alfred_server/endpoint_cfg")
async def set_alfred_server_endpoint_cfg(data: ALFRED_CONFIG):
    ...
```

#### See also

- [ALFRED_CONFIG](#alfred_config)



## set_alfred_server_final_host

[Show source in run_client_api.py:124](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L124)

#### Signature

```python
@alfred_app.post("/alfred_server/final_host")
async def set_alfred_server_final_host(request: Request):
    ...
```



## set_alfred_server_model

[Show source in run_client_api.py:96](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L96)

#### Signature

```python
@alfred_app.post("/alfred_server/model")
async def set_alfred_server_model(request: Request):
    ...
```



## set_alfred_server_model_type

[Show source in run_client_api.py:103](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L103)

#### Signature

```python
@alfred_app.post("/alfred_server/model_type")
async def set_alfred_server_model_type(request: Request):
    ...
```



## set_alfred_server_port

[Show source in run_client_api.py:89](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L89)

#### Signature

```python
@alfred_app.post("/alfred_server/port")
async def set_alfred_server_port(request: Request):
    ...
```



## set_alfred_server_username

[Show source in run_client_api.py:117](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L117)

#### Signature

```python
@alfred_app.post("/alfred_server/username")
async def set_alfred_server_username(request: Request):
    ...
```



## set_alfred_server_webhook_port

[Show source in run_client_api.py:131](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L131)

#### Signature

```python
@alfred_app.post("/alfred_server/webhook_port")
async def set_alfred_server_webhook_port(request: Request):
    ...
```



## status

[Show source in run_client_api.py:41](https://github.com/BatsResearch/alfred/blob/main/alfred/run_client_api.py#L41)

#### Signature

```python
@alfred_app.get("/status")
async def status():
    ...
```



