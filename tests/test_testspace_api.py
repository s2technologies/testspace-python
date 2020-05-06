import json
import os
import pytest
import requests

from testspace import testspace as ts


@pytest.fixture(scope="function")
def load_json(request):
    with open(os.path.join("tests", "mock_requests", request.param)) as file_handle:
        return json.load(file_handle)


@pytest.fixture(scope="function")
def testspace_api():
    token = "abcxyzfortesting"
    url = "abccorp.testspace.com"
    project = "abccorp:application"
    space = "master"
    return ts.Testspace(token, url, project, space)


@pytest.mark.parametrize("load_json", ["api_endpoints.json"], indirect=True)
def test_get_api_endpoints(load_json, testspace_api, requests_mock):
    requests_mock.get("/api", json=load_json)
    response_json = testspace_api.get_api_endpoints()

    assert response_json == load_json


@pytest.mark.parametrize("load_json", ["api_endpoints.json"], indirect=True)
def test_get_api_endpoints_url_https(load_json, testspace_api, requests_mock):
    testspace_url = "/".join([testspace_api.url, "api"])

    requests_mock.get(testspace_url, json=load_json)
    response_json = testspace_api.get_api_endpoints()

    assert response_json == load_json


@pytest.mark.parametrize("load_json", ["api_endpoints.json"], indirect=True)
def test_get_api_endpoints_username_password(load_json, requests_mock):
    token = "absmith:passfortesting"
    url = "abccorp.testspace.com"
    testspace_url = "https://{}/api".format(url)

    testspace_api = ts.Testspace(token, url)

    requests_mock.get(testspace_url, json=load_json)
    response_json = testspace_api.get_api_endpoints()

    assert response_json == load_json


@pytest.mark.parametrize("load_json", ["projects.json"], indirect=True)
def test_get_projects(load_json, testspace_api, requests_mock):
    requests_mock.get("/api/projects", json=load_json)
    response_json = testspace_api.get_projects()

    assert response_json == load_json
    project_names = [project["name"] for project in response_json]
    assert testspace_api.project in project_names


@pytest.mark.parametrize("load_json", ["projects.json"], indirect=True)
def test_get_projects_paginated(load_json, testspace_api, requests_mock):
    testspace_url = "{}/api/projects".format(testspace_api.url)

    links_string_first = '<{}?page={}>; rel="{}"'.format(testspace_url, 1, "first")
    links_string_next = '<{}?page={}>; rel="{}"'.format(testspace_url, 2, "next")
    links_string_last = '<{}?page={}>; rel="{}"'.format(testspace_url, 2, "last")

    requests_mock.get(
        "/api/projects",
        json=load_json[1:],
        headers={
            "link": ", ".join(
                [links_string_first, links_string_next, links_string_last]
            )
        },
        complete_qs=True,
    )
    requests_mock.get(
        "/api/projects?page=2",
        json=load_json[:1],
        headers={"link": ", ".join([links_string_first, links_string_last])},
    )
    response_json = testspace_api.get_projects(limit=None)

    project_names = [project["name"] for project in response_json]
    assert len(response_json) == len(load_json)
    assert testspace_api.project in project_names


@pytest.mark.parametrize("load_json", ["projects.json"], indirect=True)
def test_get_projects_paginated_limited(load_json, testspace_api, requests_mock):
    url = testspace_api.url
    testspace_url = "https://{}/api/projects".format(url)

    links_string_first = '<{}?page={}>; rel="{}"'.format(testspace_url, 1, "first")
    links_string_next = '<{}?page={}>; rel="{}"'.format(testspace_url, 2, "next")
    links_string_last = '<{}?page={}>; rel="{}"'.format(testspace_url, 2, "last")

    requests_mock.get(
        "/api/projects",
        json=load_json,
        headers={
            "link": ", ".join(
                [links_string_first, links_string_next, links_string_last]
            )
        },
        complete_qs=True,
    )

    num_projects = 1
    response_json = testspace_api.get_projects(limit=num_projects)

    assert len(response_json) == num_projects


@pytest.mark.parametrize("load_json", ["projects.json"], indirect=True)
def test_get_project_name(load_json, testspace_api, requests_mock):
    project = testspace_api.project
    project_json = [item for item in load_json if item["name"] == project][0]

    requests_mock.get("/api/projects/{}".format(project), json=project_json)
    response_json = testspace_api.get_project()

    assert project_json == load_json[0]
    assert testspace_api.project == response_json["name"]


@pytest.mark.parametrize("load_json", ["projects.json"], indirect=True)
def test_get_project_id(load_json, testspace_api, requests_mock):
    project = 66035
    project_json = [item for item in load_json if item["id"] == project][0]

    requests_mock.get("/api/projects/{}".format(project), json=project_json)
    response_json = testspace_api.get_project(project)

    assert project == response_json["id"]


def test_post_projects(testspace_api, requests_mock):
    project = "abccorp:test"
    payload = {"name": project}

    requests_mock.post("/api/projects", json=payload, status_code=201, headers=payload)
    response_json = testspace_api.post_projects(payload=payload)

    assert payload == response_json


def test_patch_project(testspace_api, requests_mock):
    payload = {"description": "CI"}
    expected_status_code = 205

    requests_mock.patch(
        "/api/projects/{}".format(testspace_api.project),
        status_code=expected_status_code,
    )
    response = testspace_api.patch_project(payload=payload)

    assert response.status_code == expected_status_code


def test_delete_project(testspace_api, requests_mock):
    expected_status_code = 204

    requests_mock.delete(
        "/api/projects/{}".format(testspace_api.project),
        status_code=expected_status_code,
    )
    response_json = testspace_api.delete_project()

    assert response_json.status_code == expected_status_code


@pytest.mark.parametrize("load_json", ["projects.json"], indirect=True)
def test_get_project_param(load_json, testspace_api, requests_mock):
    project = "abccorp:server"

    project_json = [item for item in load_json if item["name"] == project][0]

    requests_mock.get("/api/projects/{}".format(project), json=project_json)
    response_json = testspace_api.get_project(project)

    assert response_json == project_json
    assert project == response_json["name"]


def test_get_project_none(testspace_api):
    token = testspace_api.token
    url = testspace_api.url
    project = None
    testspace_api_none_project = ts.Testspace(token, url)

    with pytest.raises(Exception):
        testspace_api_none_project.get_project(project)


@pytest.mark.parametrize("load_json", ["spaces.json"], indirect=True)
def test_get_spaces(load_json, testspace_api, requests_mock):
    requests_mock.get(
        "/api/projects/{}/spaces".format(testspace_api.project), json=load_json
    )
    response_json = testspace_api.get_spaces()

    assert response_json == load_json


@pytest.mark.parametrize("load_json", ["spaces.json"], indirect=True)
def test_post_spaces(load_json, testspace_api, requests_mock):
    space = "release"
    space_json = [item for item in load_json if item["name"] == space][0]

    payload = {"name": space}
    requests_mock.post(
        "/api/projects/{}/spaces".format(testspace_api.project),
        json=space_json,
        status_code=201,
    )
    response_json = testspace_api.post_spaces(payload=payload)

    assert space == response_json["name"]


def test_patch_space(testspace_api, requests_mock):
    payload = {"description": "CI"}
    expected_status_code = 205

    requests_mock.patch(
        "/api/projects/{}/spaces/{}".format(testspace_api.project, testspace_api.space),
        status_code=expected_status_code,
    )
    response = testspace_api.patch_space(payload=payload)

    assert response.status_code == expected_status_code


def test_delete_space(testspace_api, requests_mock):
    expected_status_code = 204
    requests_mock.delete(
        "/api/projects/{}/spaces/{}".format(testspace_api.project, testspace_api.space),
        status_code=expected_status_code,
    )
    response = testspace_api.delete_space()

    assert response.status_code == expected_status_code


@pytest.mark.parametrize("load_json", ["spaces.json"], indirect=True)
def test_get_space_name(load_json, testspace_api, requests_mock):
    space = testspace_api.space

    space_json = [item for item in load_json if item["name"] == space][0]

    requests_mock.get(
        "/api/projects/{}/spaces/{}".format(testspace_api.project, space),
        json=space_json,
    )
    response_json = testspace_api.get_space()

    assert response_json == space_json
    assert space == response_json["name"]


@pytest.mark.parametrize("load_json", ["spaces.json"], indirect=True)
def test_get_space_param(load_json, testspace_api, requests_mock):
    space = "feature"
    space_json = [item for item in load_json if item["name"] == space][0]

    requests_mock.get(
        "/api/projects/{}/spaces/{}".format(testspace_api.project, space),
        json=space_json,
    )
    response_json = testspace_api.get_space(space=space)

    assert response_json == space_json
    assert space == response_json["name"]


@pytest.mark.parametrize("load_json", ["spaces.json"], indirect=True)
def test_get_space_id(load_json, testspace_api, requests_mock):
    space = 9732
    space_json = [item for item in load_json if item["id"] == space][0]

    requests_mock.get("/api/spaces/{}".format(space), json=space_json)
    response_json = testspace_api.get_space(space=space)

    assert response_json == space_json
    assert space == response_json["id"]


def test_get_space_none(testspace_api):
    token = testspace_api.token
    url = testspace_api.url
    project = testspace_api.project
    space = None

    testspace_api_none_project = ts.Testspace(token, url, project)

    with pytest.raises(Exception):
        testspace_api_none_project.get_space(space)


@pytest.mark.parametrize("load_json", ["results.json"], indirect=True)
def test_get_results(load_json, testspace_api, requests_mock):
    requests_mock.get(
        "/api/projects/{}/spaces/{}/results".format(
            testspace_api.project, testspace_api.space
        ),
        json=load_json,
    )
    response_json = testspace_api.get_results()

    assert response_json == load_json


@pytest.mark.parametrize("load_json", ["results.json"], indirect=True)
def test_get_result_name(load_json, testspace_api, requests_mock):
    result = "result.1"
    result_json = [item for item in load_json if item["name"] == result][0]

    requests_mock.get(
        "/api/projects/{}/spaces/{}/results/{}".format(
            testspace_api.project, testspace_api.space, result
        ),
        json=result_json,
    )
    response_json = testspace_api.get_result(result)

    assert response_json["name"] == result


def test_post_results(testspace_api, requests_mock):
    result_name = "result.1"
    result_json = {"id": 123456, "name": result_name}

    payload = {"name": result_name}
    requests_mock.post(
        "/api/projects/{}/spaces/{}/results".format(
            testspace_api.project, testspace_api.space
        ),
        json=result_json,
        status_code=201,
    )
    response_json = testspace_api.post_results(payload=payload)

    assert result_name == response_json["name"]


def test_delete_result_name(testspace_api, requests_mock):
    result = "result.1"
    expected_status_code = 204

    requests_mock.delete(
        "/api/projects/{}/spaces/{}/results/{}".format(
            testspace_api.project, testspace_api.space, result
        ),
        status_code=expected_status_code,
    )
    response = testspace_api.delete_result(result)

    assert response.status_code == expected_status_code


@pytest.mark.parametrize("load_json", ["results.json"], indirect=True)
def test_get_result_id(load_json, testspace_api, requests_mock):
    result = 35977
    result_json = [item for item in load_json if item["id"] == result][0]

    requests_mock.get(
        "/api/projects/{}/spaces/{}/results/{}".format(
            testspace_api.project, testspace_api.space, result
        ),
        json=result_json,
    )
    response_json = testspace_api.get_result(result)

    assert response_json["id"] == result


@pytest.mark.parametrize("load_json", ["failures.json"], indirect=True)
def test_get_result_failures(load_json, testspace_api, requests_mock):
    result = 35977

    requests_mock.get(
        "/api/projects/{}/spaces/{}/results/{}/failures".format(
            testspace_api.project, testspace_api.space, result
        ),
        json=load_json,
    )
    response_json = testspace_api.get_result_failures(result)

    assert response_json == load_json


@pytest.mark.parametrize("load_json", ["contents.json"], indirect=True)
def test_get_result_contents(load_json, testspace_api, requests_mock):
    result = 35977

    requests_mock.get(
        "/api/projects/{}/spaces/{}/results/{}/contents".format(
            testspace_api.project, testspace_api.space, result
        ),
        json=load_json,
    )
    response_json = testspace_api.get_result_contents(result)

    assert response_json == load_json


@pytest.mark.parametrize("load_json", ["contents.json"], indirect=True)
def test_get_result_contents_nested(load_json, testspace_api, requests_mock):
    result = 35977

    requests_mock.get(
        "/api/projects/{}/spaces/{}/results/{}/contents/tests".format(
            testspace_api.project, testspace_api.space, result
        ),
        json=load_json,
    )
    response_json = testspace_api.get_result_contents(result, contents_path="tests")

    assert response_json == load_json


def test_patch_result(testspace_api, requests_mock):
    result = 35977

    expected_status_code = 205
    payload = {"complete": False}
    requests_mock.patch(
        "/api/projects/{}/spaces/{}/results/{}".format(
            testspace_api.project, testspace_api.space, result
        ),
        status_code=expected_status_code,
    )
    response = testspace_api.patch_result(payload, result)

    assert response.status_code == expected_status_code


@pytest.mark.parametrize("load_json", ["metrics.json"], indirect=True)
def test_get_metrics(load_json, testspace_api, requests_mock):
    requests_mock.get(
        "/api/projects/{}/spaces/{}/metrics".format(
            testspace_api.project, testspace_api.space
        ),
        json=load_json,
    )
    response_json = testspace_api.get_metrics()

    assert response_json == load_json


@pytest.mark.parametrize("load_json", ["metrics.json"], indirect=True)
def test_get_metric_id(load_json, testspace_api, requests_mock):
    metric = 94551
    result_json = [item for item in load_json if item["id"] == metric][0]

    requests_mock.get(
        "/api/projects/{}/spaces/{}/metrics/{}".format(
            testspace_api.project, testspace_api.space, metric
        ),
        json=result_json,
    )
    response_json = testspace_api.get_metric(metric)

    assert response_json["id"] == metric


@pytest.mark.parametrize("load_json", ["metrics.json"], indirect=True)
def test_get_metric_name(load_json, testspace_api, requests_mock):
    metric = "Health"
    with pytest.raises(ValueError):
        testspace_api.get_metric(metric)


def test_post_metrics(testspace_api, requests_mock):
    metric_name = "Health"
    result_json = {"id": 123456, "name": metric_name}

    payload = {"name": metric_name}
    requests_mock.post(
        "/api/projects/{}/spaces/{}/metrics".format(
            testspace_api.project, testspace_api.space
        ),
        json=result_json,
        status_code=201,
    )
    response_json = testspace_api.post_metrics(payload=payload)

    assert metric_name == response_json["name"]


def test_delete_metric_id(testspace_api, requests_mock):
    metric = 35977
    expected_status_code = 204

    requests_mock.delete(
        "/api/projects/{}/spaces/{}/metrics/{}".format(
            testspace_api.project, testspace_api.space, metric
        ),
        status_code=expected_status_code,
    )
    response = testspace_api.delete_metric(metric)

    assert response.status_code == expected_status_code


def test_patch_metric(testspace_api, requests_mock):
    metric_id = 35977

    expected_status_code = 205
    payload = {"name": False}
    requests_mock.patch(
        "/api/projects/{}/spaces/{}/metrics/{}".format(
            testspace_api.project, testspace_api.space, metric_id
        ),
        status_code=expected_status_code,
    )
    response = testspace_api.patch_metric(payload, metric_id)

    assert response.status_code == expected_status_code


@pytest.mark.parametrize("load_json", ["metrics_datasets.json"], indirect=True)
def test_get_metric_datasets_by_id(load_json, testspace_api, requests_mock):
    metric = 34456

    requests_mock.get(
        "/api/projects/{}/spaces/{}/metrics/{}/datasets".format(
            testspace_api.project, testspace_api.space, metric
        ),
        json=load_json,
    )
    response_json = testspace_api.get_metric_datasets(metric)

    assert response_json == load_json


def test_get_status_403(testspace_api, requests_mock):
    requests_mock.get("/api", status_code=403)
    with pytest.raises(requests.exceptions.HTTPError):
        testspace_api.get_api_endpoints()


def test_get_request_json_invalid_limit(testspace_api):
    with pytest.raises(ValueError):
        testspace_api.get_request_json(limit="10")
