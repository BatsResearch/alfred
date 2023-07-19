# Utils

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Remote](./index.md#remote) /
Utils

> Auto-generated documentation for [alfred.fm.remote.utils](../../../../alfred/fm/remote/utils.py) module.

- [Utils](#utils)
  - [bytes_to_tensor](#bytes_to_tensor)
  - [get_ip](#get_ip)
  - [port_finder](#port_finder)
  - [tensor_to_bytes](#tensor_to_bytes)

## bytes_to_tensor

[Show source in utils.py:51](../../../../alfred/fm/remote/utils.py#L51)

#### Signature

```python
def bytes_to_tensor(bytes):
    ...
```



## get_ip

[Show source in utils.py:11](../../../../alfred/fm/remote/utils.py#L11)

Returns the Public IP address of the current machine.

#### Arguments

- `ipv4` - If True, returns the IPv4 address. If False, returns the IPv6 address.
:type ipv4: bool

#### Returns

The Public IP address of the current machine.
Type: *str*

#### Signature

```python
def get_ip(ipv4=True):
    ...
```



## port_finder

[Show source in utils.py:26](../../../../alfred/fm/remote/utils.py#L26)

Finds the next available port if given port is not available

#### Signature

```python
def port_finder(port: int) -> int:
    ...
```



## tensor_to_bytes

[Show source in utils.py:41](../../../../alfred/fm/remote/utils.py#L41)

#### Signature

```python
def tensor_to_bytes(tensor):
    ...
```