"""
Asses basic functionality of the Workspace endpoint.
"""
import unittest

import responses
from requests import HTTPError

from kbcstorage.workspaces import Workspaces

from tests.workspace_responses import list_response, detail_response
from tests.workspace_responses import load_tables_response, create_response
from tests.workspace_responses import reset_password_response


class TestWorkspacesEndpointWithMocks(unittest.TestCase):
    """
    Test the methods of a Workspaces endpoint instance with mock HTTP responses
    """
    def setUp(self):
        token = 'dummy_token'
        base_url = 'https://connection.keboola.com/v2/storage/'
        self.ws = Workspaces(base_url, token)

    @responses.activate
    def test_list(self):
        """
        Workspace list mocks correctly
        """
        responses.add(
            responses.Response(
                method='GET',
                url='https://connection.keboola.com/v2/storage/workspaces',
                json=list_response
            )
        )
        workspace_list = self.ws.list()
        assert isinstance(workspace_list, list)

    @responses.activate
    def test_detail_by_integer_id(self):
        """
        Workspace Endpoint can get mocked detail by integer id
        """
        responses.add(
            responses.Response(
                method='GET',
                url='https://connection.keboola.com/v2/storage/workspaces/1',
                json=detail_response
            )
        )
        workspace_id = 1
        workspace_detail = self.ws.detail(workspace_id)
        assert workspace_detail['id'] == 1

    @responses.activate
    def test_detail_by_str_id(self):
        """
        Workspace Endpoint can get mocked detail by integer id
        """
        responses.add(
            responses.Response(
                method='GET',
                url='https://connection.keboola.com/v2/storage/workspaces/1',
                json=detail_response
            )
        )
        workspace_id = '1'
        workspace_detail = self.ws.detail(workspace_id)
        assert workspace_detail['id'] == 1

    @responses.activate
    def test_detail_inexsitent_workspace(self):
        """
        Workspace Endpoint can get mocked detail by integer id
        """
        msg = ('404 Client Error: Not Found for url: '
               'https://connection.keboola.com/v2/storage/workspaces/1')
        responses.add(
            responses.Response(
                method='GET',
                url='https://connection.keboola.com/v2/storage/workspaces/1',
                body=HTTPError(msg)
            )
        )
        workspace_id = '1'
        with self.assertRaises(HTTPError) as error_context:
            self.ws.detail(workspace_id)
        assert error_context.exception.args[0] == msg

    @responses.activate
    def test_create(self):
        """
        Workspace endpoint mock creates new workspace
        """
        responses.add(
            responses.Response(
                method='POST',
                url='https://connection.keboola.com/v2/storage/workspaces',
                json=create_response
            )
        )
        created_detail = self.ws.create()
        assert created_detail['connection']['password'] == 'abc'

    @responses.activate
    def test_delete(self):
        """
        Workspace endpoint deletes mock workspace by id
        """
        responses.add(
            responses.Response(
                method='DELETE',
                url='https://connection.keboola.com/v2/storage/workspaces/1',
                json=create_response
            )
        )
        workspace_id = '1'
        deleted_detail = self.ws.delete(workspace_id)
        assert deleted_detail is None

    @responses.activate
    def test_delete_inexistent_workspace_raises_404(self):
        """
        Workspace endpoint raises 404 when mock deleting inexsitent workspace
        """
        msg = ('404 Client Error: Not Found for url: '
               'https://connection.keboola.com/v2/storage/workspaces/1')
        responses.add(
            responses.Response(
                method='DELETE',
                url='https://connection.keboola.com/v2/storage/workspaces/1',
                body=HTTPError(msg)
            )
        )
        workspace_id = '1'
        with self.assertRaises(HTTPError) as error_context:
            self.ws.delete(workspace_id)
        assert error_context.exception.args[0] == msg

    @responses.activate
    def test_load_tables_to_workspace(self):
        """
        Workspace endpoint deletes mock workspace by id
        """
        responses.add(
            responses.Response(
                method='POST',
                url=('https://connection.keboola.com/v2/storage/workspaces/'
                     '78432/load'),
                json=load_tables_response
            )
        )
        workspace_id = '78432'
        mapping = {"in.c-application-testing.cashier-data": "my-table"}
        loaded_detail = self.ws.load_tables(workspace_id, mapping)
        assert loaded_detail['id'] == 22077337

    @responses.activate
    def test_load_inexistent_tables_to_workspace(self):
        """
        Workspace endpoint deletes mock workspace by id
        """
        msg = ('404 Client Error: Not Found for url: '
               'https://connection.keboola.com/v2/storage/workspaces/78432/'
               'load')
        responses.add(
            responses.Response(
                method='POST',
                url=('https://connection.keboola.com/v2/storage/workspaces/'
                     '78432/load'),
                body=HTTPError(msg)
            )
        )
        workspace_id = '78432'
        mapping = {"in.c-table.does_not_exist": "my-table"}
        with self.assertRaises(HTTPError) as error_context:
            self.ws.load_tables(workspace_id, mapping)
        assert error_context.exception.args[0] == msg

    @responses.activate
    def test_reset_workspace_password(self):
        """
        Reset password for workspace
        """
        responses.add(
            responses.Response(
                method='POST',
                url=('https://connection.keboola.com/v2/storage/workspaces/'
                     '1/password'),
                json=reset_password_response
            )
        )
        workspace_id = '1'
        reset_detail = self.ws.reset_password(workspace_id)
        assert reset_detail['password'] == 'top_secret_password'

    @responses.activate
    def test_reset_password_for_inexistent_workspace(self):
        """
        Reset password for inexistent workspace
        """
        msg = ('404 Client Error: Not Found for url: '
               'https://connection.keboola.com/v2/storage/workspaces/1/'
               'password')
        responses.add(
            responses.Response(
                method='POST',
                url=('https://connection.keboola.com/v2/storage/workspaces/'
                     '1/password'),
                body=HTTPError(msg)
            )
        )
        workspace_id = '1'
        with self.assertRaises(HTTPError) as error_context:
            self.ws.reset_password(workspace_id)
        assert error_context.exception.args[0] == msg


if __name__ == '__main__':
    unittest.main()
