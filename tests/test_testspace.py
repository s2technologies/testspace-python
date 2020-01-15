from testspace import testspace as ts


def test_url():
    token = "abcxyzfortesting"
    url = "abccorp.testspace.com"
    project = "abccorp:application"
    space = "master"
    protocol = "https"

    testspace = ts.Testspace(token, url, project, space)
    assert testspace.url == "{}://{}".format(protocol, url)


def test_http():
    token = "abcxyzfortesting"
    url = "abccorp.testspace.com"
    project = "abccorp:application"
    space = "master"
    protocol = "http"

    testspace_url = "{}://{}".format(protocol, url)
    testspace = ts.Testspace(token, testspace_url, project, space)
    assert testspace.url == "{}://{}".format(protocol, url)
