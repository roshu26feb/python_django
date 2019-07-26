# Unit test coverage Report
> Follow the below steps to install coverage python module and generate unit test coverage report

#### Install Coverage Package
- Using pip

```sh
pip install coverage
```

- Manual installation by downloading the tar archive from pypi

```sh
pip install --no-index coverage-4.4.1.tar.gz 
```

** Note:** * should have python-devel and gcc installed before installing coverage*

#### Running Unit test
```sh
python3.5 -m coverage run setup.py test
```
#### Generating Coverage report
```sh
python3.5 -m coverage report -m
```


# Deployment build tag version for jenkins 
- User define parameter needs to be created with Parameter Name as 'deploymentTagVersion' for all component types in order to exclude from YAMl and use as deployment tag version for uri(https://{username}:{password}@{hostname}/view/{prod or non prod}/job/{pipeline_name}/view/tags/job/{deploymentTagVersion}/build)
- Following environment variable needs to be set.
    - JENKINS_HOST, (jenkins host)
    - JENKINS_API_ACCESS_USER, (jenkins API User name)
    - JENKINS_API_ACCESS_PSW, (jenkins API  password)
    - JENKINS_JOB_NAME, (jenkins job name)
    - JENKINS_PARAMETER_NAME, (jenkins parameter name to send YAML data)
    - JENKINS_DEPLOYMENT_PIPELINE_NONPROD, (non prod jenkins pipeline )
    - JENKINS_DEPLOYMENT_PIPELINE_PROD (prod jenkins pipeline)



