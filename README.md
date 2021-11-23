# testspace-python

Python module to use [Testspace](https://www.testspace.com/) API and client. Provides a python object that can manage the following Testspace items:  url, token, project name and space name. It also provides functions to push results and handle most common API requests.

## Usage
To use the module the items listed below are needed.
* Organization url (organization.testspace.com)
* [Testspace token](https://help.testspace.com/dashboard/admin-user#account)
* Project name (optional)
* Space name (optional)

Project and Space names do not have to be set on instantiation of the Testspace object and can be passed as parameters to any function call that requires them. They can also be passed into any of the functions to override, but not update the objects stored values, otherwise the stored values for project and space will be used.
```
from testspace import testspace as ts
token = "access token"
url = "organization.testspace.com"
project = "project name"
space= "space name"
testspace = ts.Testspace(token=token, url=url, project=project, space=space)
```

## Testspace Client
Provides a python wrapper to use the [Testspace client](https://help.testspace.com/reference/testspace-client) for pushing content to [Testspace](https://www.testspace.com/). Optional parameters to this function are available to provide the name of file to push, name of the result set and how.

### Example
```
testspace = ts.Testspace(token=token, url=url, project=project, space=space)
testspace.push("testresults.xml", result_name="build.1", how="full")
```
The following Testspace client [options](https://help.testspace.com/reference/testspace-client#push) are also supported as parameters to the push function.

|Client Option   | Function Parameter   |
|---|---|
|build-url|build_url|
|build-status|build_status|
|repo|repo|
|link|link|
|message|message|


## Testspace API
Provides a python wrapper for the [Testspace API](https://help.testspace.com/reference/web-api). The available functions mirror the structure of the documented API endpoints, with GET, POST, PATCH, and DELETE options available as appropriate for the endpoint. Where names in addition to id's are supported in the API, they can be used interchangably here as well. All functions return any JSON response as a result of the request, see Testspace API [help](https://help.testspace.com/reference/web-api) for details of each response. For any Testspace API that returns a list, the page size default limit of 30 is used, for any of these function the `limit` parameter can be added with an integer value for the desired maximum number of returned items. All requests are checked with raise_for_status with the expectation that any exceptions will be appropriately handled by user of the module.

### Projects
##### Get List of Projects
```
testspace.get_projects(limit=30)
```
##### Get a Project
 ```
testspace.get_project(project=None)
```
##### Create a Project
 ```
payload = {"name": "new project name"}
testspace.post_projects(payload=payload)
```
##### Update a Project
```
payload = {"description": "Awesome project"}
testspace.patch_project(payload, project=None):
```
##### Delete a Project
```
testspace.delete_project(project=None)
```
### Spaces
##### Get List of Spaces for a Project
```
testspace.get_spaces(project=None, limit=30)
```
##### Get specific space
 ```
testspace.get_space(project=None, space=None)
```
##### Create a Space
 ```
payload = {"name": "new space name"}
testspace.post_spaces(payload=payload, project=None)
```
##### Update a Space
```
payload = {"description": "Awesome project"}
testspace.patch_project(payload, project=None, space=None):
```
##### Delete a Space
```
testspace.delete_space(project=None, space=None)
```
### Results
##### Get list of Results
```
testspace.get_results(project=None, space=None, limit=30)
```
#### Get Result
```
testspace.get_result(result, project=None, space=None)
```
#### Failures
##### Get list of Result Failures
```
testspace.get_result_failures(result, project=None, space=None, limit=30)
```
#### Contents
##### Get Result Contents
```
# contents_path is used to obtain contents that are not at the root of the result
testspace.get_result_contents(result, contents_path=None, project=None, space=None, limit=30)
```
#### Metric Dataset
##### Get Metric Dataset
```
# Id must be as name resolution is not supported for metrics.
testspace.get_metric_datasets(metric, project=None, space=None, limit=30)
```
### Metrics
##### Get List of Metrics for a Space
```
testspace.get_metrics(project=None, space=None, limit=30)
```
##### Get Metric for a Space
```
# metric must be id as name resolution is not supported for this.
testspace.get_metric(metric, project=None, space=None)
```
##### Create a Space Metric
```
payload = {
  "name": "MyMetric",
  "data_source": "/path/to/suite[dataset_label]"
}
testspace.post_metrics(payload, project=None, space=None)
```
##### Update a Space Metric
```
payload = {
  "data_source": "/path/to/suite[dataset_label]"
}
testspace.patch_metrics(payload, metric, project=None, space=None)
```
##### Delete a Space Metric
```
testspace.delete_metric(metric, project=None, space=None)
```
