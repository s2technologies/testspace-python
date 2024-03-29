import pytest

from testspace import testspace as ts


@pytest.fixture(scope="function")
def testspace_client():
    token = "abcxyzfortesting"
    url = "abccorp.testspace.com"
    project = "abccorp:application"
    space = "master"
    return ts.Testspace(token, url, project, space)


def test_push(mocker, testspace_client):
    mock = mocker.patch("subprocess.run")

    file_name = "results.xml"
    result_name = "build.1"
    how = "start"
    build_url = "http://ci.com/logs.txt"
    build_status = "failure"
    build_times = "1625309472:1685986673"
    repo = "git"
    link = "coveralls"
    message = "test message"

    testspace_client.push(
        file_name,
        how=how,
        result_name=result_name,
        build_url=build_url,
        repo=repo,
        link=link,
        message=message,
        build_status=build_status,
        build_times=build_times,
    )

    url = "{}/{}/{}?{}#{}".format(
        testspace_client.url,
        testspace_client.project,
        testspace_client.space,
        how,
        result_name,
    )

    expected_push_command = ["testspace", file_name, url]
    expected_push_command.append("--build-url={}".format(build_url))
    expected_push_command.append("--repo={}".format(repo))
    expected_push_command.append("--link={}".format(link))
    expected_push_command.append("--message={}".format(message))
    expected_push_command.append("--build-status={}".format(build_status))
    expected_push_command.append("--build-times={}".format(build_times))

    mock_call_args = mock.call_args_list[0][0] # positional args of the first call
    returned_push_command = mock_call_args[0] # first positional arg
    assert expected_push_command == returned_push_command


def test_push_project_none():
    testspace = ts.Testspace(
        "abcxyzfortesting", "example.testspace.com", None, "random"
    )
    with pytest.raises(ValueError):
        testspace.push("results.xml")


def test_push_invalid_how(testspace_client):
    with pytest.raises(ValueError):
        testspace_client.push("results.xml", how="complete")
