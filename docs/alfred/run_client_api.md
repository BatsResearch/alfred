# Run Client Api

[Alfred Index](../README.md#alfred-index) /
[Alfred](./index.md#alfred) /
Run Client Api

> Auto-generated documentation for [alfred.run_client_api](../../alfred/run_client_api.py) module.

- [Run Client Api](#run-client-api)
  - [ALFRED_CONFIG](#alfred_config)
  - [alfred_server_apply_template](#alfred_server_apply_template)
  - [alfred_server_completion](#alfred_server_completion)
  - [alfred_server_completion](#alfred_server_completion-1)
  - [get_alfred_server_end_point](#get_alfred_server_end_point)
  - [get_alfred_server_final_host](#get_alfred_server_final_host)
  - [get_alfred_server_model](#get_alfred_server_model)
  - [get_alfred_server_model_type](#get_alfred_server_model_type)
  - [get_alfred_server_port](#get_alfred_server_port)
  - [get_alfred_server_username](#get_alfred_server_username)
  - [get_alfred_server_webhook_port](#get_alfred_server_webhook_port)
  - [main](#main)
  - [root](#root)
  - [set_alfred_server_connected](#set_alfred_server_connected)
  - [set_alfred_server_connected](#set_alfred_server_connected-1)
  - [set_alfred_server_end_point](#set_alfred_server_end_point)
  - [set_alfred_server_endpoint_cfg](#set_alfred_server_endpoint_cfg)
  - [set_alfred_server_final_host](#set_alfred_server_final_host)
  - [set_alfred_server_model](#set_alfred_server_model)
  - [set_alfred_server_model_type](#set_alfred_server_model_type)
  - [set_alfred_server_port](#set_alfred_server_port)
  - [set_alfred_server_username](#set_alfred_server_username)
  - [set_alfred_server_webhook_port](#set_alfred_server_webhook_port)
  - [status](#status)

## ALFRED_CONFIG

[Show source in run_client_api.py:32](../../alfred/run_client_api.py#L32)

#### Signature

```python
class ALFRED_CONFIG(BaseModel):
    ...
```



## alfred_server_apply_template

[Show source in run_client_api.py:244](../../alfred/run_client_api.py#L244)

#### Signature

```python
@alfred_app.post("/alfred_server/apply_template")
async def alfred_server_apply_template(request: Request):
    ...
```



## alfred_server_completion

[Show source in run_client_api.py:219](../../alfred/run_client_api.py#L219)

#### Signature

```python
@alfred_app.post("/alfred_server/completion")
async def alfred_server_completion(request: Request):
    ...
```



## alfred_server_completion

[Show source in run_client_api.py:230](../../alfred/run_client_api.py#L230)

#### Signature

```python
@alfred_app.post("/alfred_server/rank")
async def alfred_server_completion(request: Request):
    ...
```



## get_alfred_server_end_point

[Show source in run_client_api.py:67](../../alfred/run_client_api.py#L67)

#### Signature

```python
@alfred_app.get("/alfred_server/end_point")
async def get_alfred_server_end_point():
    ...
```



## get_alfred_server_final_host

[Show source in run_client_api.py:77](../../alfred/run_client_api.py#L77)

#### Signature

```python
@alfred_app.get("/alfred_server/final_host")
async def get_alfred_server_final_host():
    ...
```



## get_alfred_server_model

[Show source in run_client_api.py:57](../../alfred/run_client_api.py#L57)

#### Signature

```python
@alfred_app.get("/alfred_server/model")
async def get_alfred_server_model():
    ...
```



## get_alfred_server_model_type

[Show source in run_client_api.py:62](../../alfred/run_client_api.py#L62)

#### Signature

```python
@alfred_app.get("/alfred_server/model_type")
async def get_alfred_server_model_type():
    ...
```



## get_alfred_server_port

[Show source in run_client_api.py:52](../../alfred/run_client_api.py#L52)

#### Signature

```python
@alfred_app.get("/alfred_server/port")
async def get_alfred_server_port():
    ...
```



## get_alfred_server_username

[Show source in run_client_api.py:72](../../alfred/run_client_api.py#L72)

#### Signature

```python
@alfred_app.get("/alfred_server/username")
async def get_alfred_server_username():
    ...
```



## get_alfred_server_webhook_port

[Show source in run_client_api.py:82](../../alfred/run_client_api.py#L82)

#### Signature

```python
@alfred_app.get("/alfred_server/webhook_port")
async def get_alfred_server_webhook_port():
    ...
```



## main

[Show source in run_client_api.py:270](../../alfred/run_client_api.py#L270)

#### Signature

```python
def main(args):
    ...
```



## root

[Show source in run_client_api.py:41](../../alfred/run_client_api.py#L41)

#### Signature

```python
@alfred_app.get("/")
async def root():
    ...
```



## set_alfred_server_connected

[Show source in run_client_api.py:87](../../alfred/run_client_api.py#L87)

#### Signature

```python
@alfred_app.get("/alfred_server/connected")
async def set_alfred_server_connected():
    ...
```



## set_alfred_server_connected

[Show source in run_client_api.py:258](../../alfred/run_client_api.py#L258)

#### Signature

```python
@alfred_app.get("/alfred_server/cache")
async def set_alfred_server_connected():
    ...
```



## set_alfred_server_end_point

[Show source in run_client_api.py:115](../../alfred/run_client_api.py#L115)

#### Signature

```python
@alfred_app.post("/alfred_server/end_point")
async def set_alfred_server_end_point(request: Request):
    ...
```



## set_alfred_server_endpoint_cfg

[Show source in run_client_api.py:148](../../alfred/run_client_api.py#L148)

#### Signature

```python
@alfred_app.post("/alfred_server/endpoint_cfg")
async def set_alfred_server_endpoint_cfg(data: ALFRED_CONFIG):
    ...
```

#### See also

- [ALFRED_CONFIG](#alfred_config)



## set_alfred_server_final_host

[Show source in run_client_api.py:129](../../alfred/run_client_api.py#L129)

#### Signature

```python
@alfred_app.post("/alfred_server/final_host")
async def set_alfred_server_final_host(request: Request):
    ...
```



## set_alfred_server_model

[Show source in run_client_api.py:101](../../alfred/run_client_api.py#L101)

#### Signature

```python
@alfred_app.post("/alfred_server/model")
async def set_alfred_server_model(request: Request):
    ...
```



## set_alfred_server_model_type

[Show source in run_client_api.py:108](../../alfred/run_client_api.py#L108)

#### Signature

```python
@alfred_app.post("/alfred_server/model_type")
async def set_alfred_server_model_type(request: Request):
    ...
```



## set_alfred_server_port

[Show source in run_client_api.py:94](../../alfred/run_client_api.py#L94)

#### Signature

```python
@alfred_app.post("/alfred_server/port")
async def set_alfred_server_port(request: Request):
    ...
```



## set_alfred_server_username

[Show source in run_client_api.py:122](../../alfred/run_client_api.py#L122)

#### Signature

```python
@alfred_app.post("/alfred_server/username")
async def set_alfred_server_username(request: Request):
    ...
```



## set_alfred_server_webhook_port

[Show source in run_client_api.py:136](../../alfred/run_client_api.py#L136)

#### Signature

```python
@alfred_app.post("/alfred_server/webhook_port")
async def set_alfred_server_webhook_port(request: Request):
    ...
```



## status

[Show source in run_client_api.py:46](../../alfred/run_client_api.py#L46)

#### Signature

```python
@alfred_app.get("/status")
async def status():
    ...
```


