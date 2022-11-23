"""convertio.py - Lightweight Python wrapper for the Convertio  API.

This module provide 2 main classess, Client and Conversion. Client
is initialized with the API key and can be used to create new 
Conversion objects.

Example
-------
    import convertio
    api = convertio.Client (open (".apiKey", "r").read ())
    conversion = api.convert ("./nvl.epub", "pdf")
    conversion.download ("./n.pdf").delete ()
"""

import requests, time, secrets
from validators import url as validate_url
from pathlib import Path
from urllib.parse import urlparse
from os.path import basename

class APIError (Exception):
    """Error for when Convertio API returns an error"""
    pass

class Conversion(object):
    def __init__(self, client, conversion_id):
        self.id, self.client = conversion_id, client

    def get_status (self):
        return self.client.get_status(self.id)

    def download (self, dest = None, timeout = 1e9):
        self.client.download (self.id, dest) 
        return self

    def delete (self):
        self.client.delete (self.id)

    def wait (timeout = 1e9):
        self.client.wait (timeout)
        return self

class Client(object):
    API_HOST = "https://api.convertio.co"

    def __init__ (self, api_key):
        self.api_key = api_key

    def _request (self, method, path, ** kwargs):
        r = requests.request (method, self.API_HOST + path, **kwargs)
        r.raise_for_status()
        data = r.json ()
        if data ["status"] != "ok": raise APIError(data ["error"])
        return data ["data"]

    def _save (self, url, output):
        with requests.get (url, stream = True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=4096):
                output.write (chunk)

    def get_balance (self):
        return self._request("POST", "/balance", 
                json = {"apikey" : self.api_key})["minutes_left"]

    def convert (self, source, output_format, ** kwargs): 
        """Start a new conversion. 

        `source` can be an url, path or file-like object. 
        Optionnal keyword-only arguments:
            - `filename`: give another name to the file.
            - `options`: dict of options .
        Examples:
            convert ("./nvl.epub", "pdf", options = {
                "callback_url" : "https://example.com/hook"
            })
            convert ("https://google.com", "epub", filename = "g.html")
        """
        req_body = {
                "apikey" : self.api_key,
                "outputformat" : output_format
                }
        if isinstance(source, str) and validate_url (source):
            req_body ["input"], req_body ["file"] = "url", source
        else:
            req_body ["input"] = "upload"
            if isinstance(source, (str, Path)):
                p = Path (source)
                if p.exists () and p.is_file ():
                    source = p.open ("rb")
                else: raise ValueError ("Invalid file")

        if "filename" in kwargs:
            req_body ["filename"] = kwargs ["filename"]
        else:
            if hasattr(source, "name"):
                req_body["filename"] = source.name
            else: req_body ["filename"] = secrets.token_hex (16)
        if ("options" in kwargs and 
                isinstance (kwargs["options"], dict) and 
                len (kwargs["options"]) > 0):
            req_body ["options"] = kwargs ["options"]
        data = self._request ("POST", "/convert", json = req_body)
        conv = Conversion (self, data ["id"])
        if req_body["input"] == "upload":
            self._request ("PUT", 
                    f'/convert/{conv.id}/{req_body ["filename"]}',
                    files = {req_body ["filename"] : source})
        return conv

    def list_conversions (self, count = 10, status  = "all"):
        return self._request ("POST", "/convert/list", json = 
                {"apikey" : self.api_key,"count" : count,"status" : status})

    def get_status (self, conversion_id):
        return self._request ("GET", f"/convert/{conversion_id}/status")

    def delete (self, conversion_id):
        self._request ("DELETE", f"/convert/{conversion_id}")

    def wait (self, conversion_id, timeout = 1e9):
        """Wait until the conversion output file is ready.

        TimeoutError will be raised if the conversion is not 
        finished after  `timeout` seconds spent waiting.
        """
        start = time.time ()
        status = self.get_status (conversion_id)
        if status ["step"] == "finish": return self
        while time.time () - start < timeout:
            status = self.get_status (conversion_id)
            if status ["step"] == "finish": return self
            else: time.sleep (0.5)
        raise TimeoutError ("File not ready yet")

    def download (self, conversion_id, dest = None, timeout = 1e9):
        """Download the ouput file to the given destination.

        `dest` is a string or file-like object. If there is more than 
        one output file and `dest` is a directory, the files will be 
        downloaded separately into it. If not set, it default to file
        name.
        The function will wait for at most `timeout` before raising 
        an error if the file is not ready for download.
        """
        self.wait (conversion_id, timeout)
        status = self.get_status (conversion_id)
        url = status ["output"]["url"]
        if dest == None:
            dest = open (basename(urlparse(url).path), "wb")
        if not isinstance(dest, (str, Path)): self._save (url, dest)
        else:
            dest = Path (dest)
            if not dest.is_dir (): 
                dest = dest.open ("wb")
                self._save (url, dest)
            else:
                if "files" in status ["output"]:
                    for file in status ["output"]["files"]:
                        self._save (f"{url}/{file}",
                                dest.joinpath(file).open ("wb"))
                else: self._save (url, 
                        dest.joinpath (
                            basename(urlparse(url).path)).open ("wb"))
