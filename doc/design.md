# Design: Jenkins Hub

## Components

The Jenkins Hub consists of the following components:

* Service configuration: the service configuration is handled by this component.
* Jenkins synchronizer: this component synchronizes the information with Jenkins masters configured.
* Data generator: this component generates the JSON files to represent the Jenkins masters.
* HTTP daemon: allow the service consumers to call.

## The JSON data format for a Jenkins master

master
  [master info]
  slaves:
    slave...
    slave...
    ...
  jobs:
    job...
    job...
    ...