import json
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import requests
import yaml
from actions import Action
from storage import Storage

DIVIDER = "-" * 50
SHORT_DIVIDER = "-" * 10


class VariableItem:
    def __init__(self, item):
        for k, v in item.items():
            if isinstance(v, dict):
                v = VariableItem(v)
            setattr(self, k, v)


@dataclass
class Request:
    method: str
    url: str
    headers: Optional[Dict[str, str]] = None
    json: Optional[dict] = None
    query_params: Optional[Dict[str, str]] = None
    print: Callable = print
    post_response: Optional[dict] = None

    @classmethod
    def new_request(cls, requests_filename, request_name, env):
        with open(requests_filename, "r") as file:
            data = yaml.safe_load(file)

        request_data = cls.nested_get(data, request_name.split("."))

        if request_data is None:
            raise ValueError(f"Request {request_name} not found")

        return cls(**request_data, print=print).replace(cls.get_variables(data, env))

    @classmethod
    def get_variables(cls, data, env):
        variables = data.get("variables", {})

        if env:
            variables = {**variables, **data.get("envs", {}).get(env, {}).get("variables", {})}

        variables["storage"] = Storage.read()

        for k, v in variables.items():
            if isinstance(v, dict):
                v = VariableItem(v)
                variables[k] = v

        return variables

    @classmethod
    def nested_get(cls, data: dict, keys: List[str]):
        if not isinstance(data, dict):
            return None

        if not keys:
            return data

        return cls.nested_get(data.get(keys[0]), keys[1:])

    def send(self):
        self.log("request", self.json)
        response = requests.request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            json=self.json,
            params=self.query_params,
        )
        try:
            self.log("response", json.dumps(response.json(), indent=2), {"status code": response.status_code})
            if self.post_response:
                Action.new_action(self.post_response).do(response.json())
        except Exception:
            self.log("response", response.text, {"status code": response.status_code})

    def replace(self, variables: Dict[str, VariableItem]):
        def render(x):
            return x.format(**variables) if isinstance(x, str) else x

        self.url = render(self.url)

        if self.headers and isinstance(self.headers, dict):
            self.walk(self.headers, render)

        if self.query_params and isinstance(self.query_params, dict):
            self.walk(self.query_params, render)

        if self.json and isinstance(self.json, dict):
            self.walk(self.json, render)

        return self

    @classmethod
    def walk(cls, d: dict, visit: Callable):
        for k in d:
            d[k] = cls.walk(d[k], visit) if isinstance(d[k], dict) else visit(d[k])

        return d

    def log(self, name, data, metadata=None):
        metadata_text = ""

        if metadata:
            for k, v in metadata.items():
                metadata_text += f"{k}: {v}\n"

        if metadata_text:
            metadata_text = f"metadata\n{metadata_text}{SHORT_DIVIDER}"

        if isinstance(data, str):
            data_text = data
        else:
            data_text = json.dumps(data, indent=2)

        self.print(f"{name}\n{DIVIDER}\n{metadata_text}\n{data_text}\n{DIVIDER}\n\n")
