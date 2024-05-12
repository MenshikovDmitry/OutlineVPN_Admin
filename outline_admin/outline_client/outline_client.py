from outline_vpn.outline_vpn import OutlineVPN

class OutlineClient:
    def __init__(self, api_url, api_token):
        self.api_url = api_url
        self.api_token = api_token
        self.client = OutlineVPN(api_url, api_token)

    def get_keys(self):
        resp = self.client.get_keys()
        out_data = []
        for key in resp:
            k = key.__dict__
            k['data_limit_mb'] = k['data_limit'] / 1000 / 1000 if k['data_limit'] else None
            k['used_mb'] = k['used_bytes'] / 1000 / 1000 if k['used_bytes'] else 0
            k['usage'] = round( k['used_mb'] / k['data_limit_mb'] * 100) if k['data_limit_mb'] else 0
            out_data.append(k)
        return {'keys': out_data}

    def add_key(self, name, data_limit_mb=None):
        new_key = self.client.create_key()
        self.client.rename_key(new_key.key_id, name)
        if data_limit_mb is not None:
            self.client.add_data_limit(new_key.key_id, data_limit_mb * 1000 * 1000)
        return new_key

    def remove_key(self, key_id):
        self.client.delete_key(key_id)

    def set_data_limit(self, key_id, data_limit_mb):
        self.client.add_data_limit(key_id, data_limit_mb * 1000 * 1000)
        return True
