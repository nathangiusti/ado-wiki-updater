import os
import sys

import requests
import yaml


def main():

    files = sys.argv[1]
    config = sys.argv[2]
    tenant_id = sys.argv[3]
    organization = sys.argv[4]  #'abi-ghq-audit-dsc-dev-ops'
    project = sys.argv[5]  #'beer_tech'
    wiki_id = sys.argv[6]  #'beer_tech.wiki'
    seperator = sys.argv[7]

    with open(config, 'r') as yml_file:
        cfg = yaml.safe_load(yml_file)

    data = {
        'client_id': os.environ['CLIENT_ID'],
        'grant_type': 'client_credentials',
        'scope': 'https://graph.microsoft.com/.default',
        'response_mode': 'query',
        'client_secret': os.environ['CLIENT_SECRET']
    }

    response = requests.get('https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(tenant_id), data=data)
    access_token = response.json()['access_token']
    token = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    for file in files.split(seperator):
        if file.endswith('.md') and os.path.exists(file) and file in cfg:
            page_id = cfg[file]
            with open(file) as f:
                lines = f.read()
            wiki_content = {"content":  lines}
            url = f'https://dev.azure.com/{organization}/{project}/_apis/wiki/wikis/{wiki_id}/pages/{page_id}?api-version=6.0-preview.1'
            print(url)
            response = requests.patch(url,
                                      headers=token, json=wiki_content)

            if response.status_code not in [200, 201, 202, 204]:
                raise Exception('ERROR: {}: {}\nURL: {}'.format(response.status_code, response.content, response.url))


if __name__ == '__main__':
    main()
