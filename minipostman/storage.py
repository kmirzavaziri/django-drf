import json
import os


class Storage:
    @staticmethod
    def read():
        if not os.path.exists(".storage"):
            return {}

        with open(".storage") as f:
            return json.load(f)

    @staticmethod
    def append(d: dict):
        json_data = Storage.read()

        for k, v in d.items():
            json_data[k] = v

        with open(".storage", "w") as f:
            json.dump(json_data, f, indent=2)
