from flask_restful import Resource, reqparse

from config import API_URL, API_TOKEN
from outline_admin.outline_client.outline_client import OutlineClient


create_key_parser = reqparse.RequestParser()
create_key_parser.add_argument('name', type=str,
                    required=True,
                    help='Name of the key, {error_msg}.',
                    location=('json', 'values',) )
create_key_parser.add_argument('data_limit_mb', type=int,
                    required=False,
                    help='Data limit in MB, {error_msg}.',
                    location=('json', 'values',) )


remove_key_parser = reqparse.RequestParser()
remove_key_parser.add_argument('key_id', type=str,
                    required=True,
                    help='Key ID, {error_msg}.',
                    location=('json', 'values',) )

set_limit_parser = reqparse.RequestParser()
set_limit_parser.add_argument('key_id', type=str,
                    required=True,
                    help='Key ID, {error_msg}.',
                    location=('json', 'values',) )
set_limit_parser.add_argument('data_limit_mb', type=int,
                    required=True,
                    help='Data limit in MB, {error_msg}.',
                    location=('json', 'values',) )


class OutlineResource(Resource):
    """Flask API Resource wrapper for the Outline"""
    def __init__(self):
        self.client = OutlineClient(API_URL, API_TOKEN)

    def get(self, cmd):
        if cmd == 'get_keys':
            return self.client.get_keys()

    def post(self, cmd):
        if cmd == 'create_key':
            args = create_key_parser.parse_args()
            if self.client.add_key(args['name'], args['data_limit_mb']) == True:
                return {'success': 'true', 'message': 'Key created successfully.'}
            return False
        elif cmd == 'remove_key':
            args = remove_key_parser.parse_args()
            if self.client.remove_key(args['key_id']) == True:
                return {'success': 'true', 'message': 'Key removed successfully.'}
            return False
        elif cmd == 'set_data_limit':
            args = set_limit_parser.parse_args()
            if self.client.set_data_limit(args['key_id'], args['data_limit_mb']) == True:
                return {'success': 'true', 'message': 'Data limit set successfully.'}
            return False


