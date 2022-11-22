# Convertio API's client library in Python

Small wrapper for the Convertio file conversion API. Feel free to do whatever you want with it.
You can read the full API docs [here](https://convertio.co/api/docs/).

## Requirements

- [validators](https://github.com/python-validators/validators)

## Example 

```python3
import convertio
api = convertio.Client (open (".apiKey", "r").read ())
conversion = api.convert ("./nvl.epub", "pdf", options = {"callback_url": "https://path/to/endpoint"})
conversion.download ("./n.pdf").delete ()
```

