from testspace import testspace as ts


def test_url_token():
    token = "abcxyzfortesting"
    url = "abccorp.testspace.com"
    project = "abccorp:application"
    space = "master"
    protocol = "https"

    client_url = "{}:@{}".format(token, url)
    api_url = "{}://{}/api".format(protocol, url)

    testspace = ts.Testspace(token, url, project, space)
    assert testspace.client_url == client_url
    assert testspace.api_url == api_url


def test_url_password():
    token = "absmith:passfortesting"
    url = "abccorp.testspace.com"
    project = "abccorp:application"
    space = "master"
    protocol = "https"

    client_url = "{}@{}".format(token, url)
    api_url = "{}://{}/api".format(protocol, url)

    testspace = ts.Testspace(token, url, project, space)
    assert testspace.client_url == client_url
    assert testspace.api_url == api_url


def test_http():
    token = "abcxyzfortesting"
    url = "abccorp.testspace.com"
    project = "abccorp:application"
    space = "master"
    protocol = "http"

    client_url = "{}://{}:@{}".format(protocol, token, url)
    api_url = "{}://{}/api".format(protocol, url)

    testspace_url = "{}://{}".format(protocol, url)
    testspace = ts.Testspace(token, testspace_url, project, space)
    assert testspace.client_url == client_url
    assert testspace.api_url == api_url
