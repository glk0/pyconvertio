# Convertio API's client library in Python
------------------------------------------

Small wrapper for the Convertio file conversion API. Feel free to do whatever you want with it.
You can read the full API docs [here](https://convertio.co/api/docs/).

# Requriements

[validators](https://github.com/python-validators/validators)

# Example 

```python3
import convertio
api = convertio.Client (open (".apiKey", "r").read ())
conversion = api.convert ("./nvl.epub", "pdf")
conversion.download ("./n.pdf").delete ()
```

