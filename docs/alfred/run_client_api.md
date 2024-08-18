# Run Client Api

[Alfred Index](../README.md#alfred-index) / [Alfred](./index.md#alfred) / Run Client Api

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
  - [get_cache_table](#get_cache_table)
  - [main](#main)
  - [root](#root)
  - [set_alfred_server_connected](#set_alfred_server_connected)
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

[Show source in run_client_api.py:31](../../alfred/run_client_api.py#L31)

#### Signature

```python
class ALFRED_CONFIG(BaseModel): ...
```



## alfred_server_apply_template

[Show source in run_client_api.py:247](../../alfred/run_client_api.py#L247)

#### Signature

```python
@alfred_app.post("/alfred_server/apply_template")
async def alfred_server_apply_template(request: Request): ...
```



## alfred_server_completion

[Show source in run_client_api.py:221](../../alfred/run_client_api.py#L221)

#### Signature

```python
@alfred_app.post("/alfred_server/completion")
async def alfred_server_completion(request: Request): ...
```



## alfred_server_completion

[Show source in run_client_api.py:232](../../alfred/run_client_api.py#L232)

#### Signature

```python
@alfred_app.post("/alfred_server/rank")
async def alfred_server_completion(request: Request): ...
```



## get_alfred_server_end_point

[Show source in run_client_api.py:66](../../alfred/run_client_api.py#L66)

#### Signature

```python
@alfred_app.get("/alfred_server/end_point")
async def get_alfred_server_end_point(): ...
```



## get_alfred_server_final_host

[Show source in run_client_api.py:76](../../alfred/run_client_api.py#L76)

#### Signature

```python
@alfred_app.get("/alfred_server/final_host")
async def get_alfred_server_final_host(): ...
```



## get_alfred_server_model

[Show source in run_client_api.py:56](../../alfred/run_client_api.py#L56)

#### Signature

```python
@alfred_app.get("/alfred_server/model")
async def get_alfred_server_model(): ...
```



## get_alfred_server_model_type

[Show source in run_client_api.py:61](../../alfred/run_client_api.py#L61)

#### Signature

```python
@alfred_app.get("/alfred_server/model_type")
async def get_alfred_server_model_type(): ...
```



## get_alfred_server_port

[Show source in run_client_api.py:51](../../alfred/run_client_api.py#L51)

#### Signature

```python
@alfred_app.get("/alfred_server/port")
async def get_alfred_server_port(): ...
```



## get_alfred_server_username

[Show source in run_client_api.py:71](../../alfred/run_client_api.py#L71)

#### Signature

```python
@alfred_app.get("/alfred_server/username")
async def get_alfred_server_username(): ...
```



## get_alfred_server_webhook_port

[Show source in run_client_api.py:81](../../alfred/run_client_api.py#L81)

#### Signature

```python
@alfred_app.get("/alfred_server/webhook_port")
async def get_alfred_server_webhook_port(): ...
```



## get_cache_table

[Show source in run_client_api.py:261](../../alfred/run_client_api.py#L261)

#### Signature

```python
@alfred_app.get("/alfred_server/cache")
async def get_cache_table(): ...
```



## main

[Show source in run_client_api.py:273](../../alfred/run_client_api.py#L273)

#### Signature

```python
def main(args): ...
```



## root

[Show source in run_client_api.py:40](../../alfred/run_client_api.py#L40)

#### Signature

```python
@alfred_app.get("/")
async def root(): ...
```



## set_alfred_server_connected

[Show source in run_client_api.py:86](../../alfred/run_client_api.py#L86)

#### Signature

```python
@alfred_app.get("/alfred_server/connected")
async def set_alfred_server_connected(): ...
```



## set_alfred_server_end_point

[Show source in run_client_api.py:114](../../alfred/run_client_api.py#L114)

#### Signature

```python
@alfred_app.post("/alfred_server/end_point")
async def set_alfred_server_end_point(request: Request): ...
```



## set_alfred_server_endpoint_cfg

[Show source in run_client_api.py:148](../../alfred/run_client_api.py#L148)

#### Signature

```python
@alfred_app.post("/alfred_server/endpoint_cfg")
async def set_alfred_server_endpoint_cfg(data: ALFRED_CONFIG): ...
```

#### See also

- [ALFRED_CONFIG](#alfred_config)



## set_alfred_server_final_host

[Show source in run_client_api.py:128](../../alfred/run_client_api.py#L128)

#### Signature

```python
@alfred_app.post("/alfred_server/final_host")
async def set_alfred_server_final_host(request: Request): ...
```



## set_alfred_server_model

[Show source in run_client_api.py:100](../../alfred/run_client_api.py#L100)

#### Signature

```python
@alfred_app.post("/alfred_server/model")
async def set_alfred_server_model(request: Request): ...
```



## set_alfred_server_model_type

[Show source in run_client_api.py:107](../../alfred/run_client_api.py#L107)

#### Signature

```python
@alfred_app.post("/alfred_server/model_type")
async def set_alfred_server_model_type(request: Request): ...
```



## set_alfred_server_port

[Show source in run_client_api.py:93](../../alfred/run_client_api.py#L93)

#### Signature

```python
@alfred_app.post("/alfred_server/port")
async def set_alfred_server_port(request: Request): ...
```



## set_alfred_server_username

[Show source in run_client_api.py:121](../../alfred/run_client_api.py#L121)

#### Signature

```python
@alfred_app.post("/alfred_server/username")
async def set_alfred_server_username(request: Request): ...
```



## set_alfred_server_webhook_port

[Show source in run_client_api.py:135](../../alfred/run_client_api.py#L135)

#### Signature

```python
@alfred_app.post("/alfred_server/webhook_port")
async def set_alfred_server_webhook_port(request: Request): ...
```



## status

[Show source in run_client_api.py:45](../../alfred/run_client_api.py#L45)

#### Signature

```python
@alfred_app.get("/status")
async def status(): ...
```