# pyconvertio - Convertio API wrapper

**pyconvertio** is a small wrapper for the Convertio file conversion API. It provides just two
classes, `Client` and `Conversion` that allows to start conversions, monitor them and download
the output file.<br>
For more information, you can read the full Convertio API docs [here](https://convertio.co/api/docs/).

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
