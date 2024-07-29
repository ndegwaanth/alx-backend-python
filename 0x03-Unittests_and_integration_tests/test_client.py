#!/usr/bin/env python3
'''Module testing the GithubOrgClient class.
'''
from parameterized import parameterized, parameterized_class  # type: ignore
import unittest
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from typing import Mapping, Sequence
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    '''Unit test class for GithubOrgClient.
    '''
    @parameterized.expand(['google', 'abc'])
    @patch('requests.get')
    def test_org(self, org_name: str, mock_get: Mock) -> None:
        '''Tests the org method.
        '''
        mock_response = Mock()
        mock_response.json.return_value = {'repos_url': 'https://example.com'}
        mock_get.return_value = mock_response
        instance = GithubOrgClient(org_name)
        r_value = instance.org
        self.assertEqual(r_value, {'repos_url': 'https://example.com'})
        mock_get.assert_called_once_with(
            f'https://api.github.com/orgs/{org_name}'
        )

    def test_public_repos_url(self) -> None:
        '''Tests the _public_repos_url property.
        '''
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {'repos_url': 'https://example.com'}
            instance = GithubOrgClient('my_Org')
            r_value = instance._public_repos_url
            self.assertEqual(r_value, 'https://example.com')

    @patch('requests.get')
    def test_public_repos(self, mock_get: Mock) -> None:
        '''Tests the public_repos method.
        '''
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = 'https://api.github.com/repos'
            mock_response = Mock()
            mock_response.json.return_value = [
                {'name': 'repo1'}, {'name': 'repo2'}
            ]
            mock_get.return_value = mock_response
            instance = GithubOrgClient('my_Org')
            r_value = instance.public_repos()
            self.assertEqual(r_value, ['repo1', 'repo2'])
            mock_url.assert_called_once()
            mock_get.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: dict, license_key: str,
                         expected: bool) -> None:
        '''Tests the has_license method.
        '''
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''Integration tests for the GithubOrgClient class.
    '''
    @classmethod
    @patch('requests.get')
    def setUpClass(cls, mock_get: Mock) -> None:
        '''Sets up class for integration tests.
        '''
        cls.get_patcher = patch('requests.get')
        cls.mock_response = cls.get_patcher.start()

        def side_effect(url: str) -> Mock:
            '''Returns a mock response based on URL.
            '''
            mock_response = Mock()
            if 'orgs' in url:
                mock_response.json.return_value = cls.org_payload
            elif 'repos' in url:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_response.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        '''Cleans up after tests.
        '''
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        '''Integration test for public_repos.
        '''
        instance = GithubOrgClient('my_Org')
        result = instance.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        '''Integration test for public_repos with license filter.
        '''
        instance = GithubOrgClient('my_Org')
        result = instance.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
