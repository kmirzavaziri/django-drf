from storage import Storage


class Action:
    @staticmethod
    def new_action(action_data):
        if "store" in action_data:
            return StoreAction(action_data["store"])


class StoreAction:
    def __init__(self, action_data):
        self.items = action_data

    def do(self, data):
        storage_data = {}
        for item in self.items:
            storage_data[item["to"]] = data.get(item["from"])

        Storage.append(storage_data)
