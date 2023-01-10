# Pyconvertio: Convertio API client library in Python

Pyconvertio is a small wrapper for the Convertio file conversion API. Feel free to do whatever you want with it.
You can read the full API docs [here](https://convertio.co/api/docs/).

## Requirements

- [validators](https://github.com/python-validators/validators)

## Examples

### Simple EPUB to PDF conversion

```python3
import pyconvertio
api = pyconvertio.Client (open (".apiKey", "r").read ())
conversion = api.convert ("./nvl.epub", "pdf")
conversion.download ().delete ()
```

### Convert online HTML to JPG

```python3
api.convert ("https://google.com", "jpg").download (dest = "g.jpg")
```
