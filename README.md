# Web Application Metrics

## Overview
The Web Application Metrics (WAM) project was developed to provide an automated method to capture performance metrics from the user perspective for a suite of web actions on a given web app.  The web actions can be customized for any web application and can be executed in a variety of scenarios for flexibility.  The WAM project utilizes a docker container to execute the actions with [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/).

## Resources
-   WAM Version Control Information:
    -   URL: git@github.com:noaa-pifsc/PIFSC-Tools-Web-App-Metrics.git
    -   Version: 1.4 (Git tag: web_app_metrics_v1.4)

## Scenarios
-   There are three different scenarios implemented by the docker project:
    -   Local - this scenario deploys the docker container to a local docker host and connects to a local web app
    -   Remote - this scenario deploys the docker container to a remote docker host and connects to a remote web app
    -   Hybrid - this scenario deploys the docker container to a local docker host and connects to a remote web app

## Setup Procedure
-   ### Standalone Implementation
    -   \*Note: this implementation option is provided for standalone execution, where this repository is cloned and prepared for deployment and the user updates the appropriate files below and builds/runs the container  
    -   Clone the WAM repository to a working directory
    -   Update the bash script deployment configuration file ([project_deploy_config.sh](./docker/src/sh_scripts/config/project_deploy_config.sh)) with the appropriate values:
        -   project_path is the folder name of the working copy of the repository that will be used to build the container
        -   git_url is the project git URL value
    -   Execute the appropriate docker preparation script stored in the [deployment_scripts](./deployment_scripts) folder to prepare the docker container for deployment in a new working directory
        -   For example use the [prepare_docker_project.local.sh](./deployment_scripts/prepare_docker_project.local.sh) bash script to prepare the Local docker container for deployment in the c:/docker/web-app-metrics-local folder
    -   Optional updates:
        -   Update the docker compose runtime configuration file (e.g. c:/docker/web-app-metrics-local/docker/docker-compose.prod.yml) to specify repository-specific the volume names and container name
        -   Update the docker compose configuration file (e.g. c:/docker/web-app-metrics-local/docker/docker-compose.yml) to specify the volume names and image/container names for the forked project
    -   Update the login_credentials.py file in the appropriate new working directory to specify the username and password for the given web application (e.g. c:/docker/web-app-metrics-local/docker/py_scripts/lib/login_credentials.py) for the local scenario
        -   \*\*Note: Do not commit the login credentials for the given web application in the repository for security reasons
    -   Update the app_config.py file in the appropriate new working directory to specify the configuration values for the given web application (e.g. c:/docker/web-app-metrics-local/docker/py_scripts/lib/app_config.py) for the local scenario, comments are defined in the configuration file to describe the configuration variables that should be defined.
    -   Update the [app.py](./docker/src/py_scripts/app.py) to define the web actions to execute for the given web app, to capture the elapsed time for each web action, and log the standard metrics in the defined .csv file.
        -   There is a block comment defined in app.py that indicates where the custom code should be defined for a given web app
-   ### Forked Repository Implementation
    -   \*Note: this repository can be forked for a specific database instance/schema to make it easier to build and deploy the container to capture metrics for a given database instance/schema.
        -   [WAM - IBBS](https://github.com/noaa-pifsc/PIFSC-Tools-Web-App-Metrics-IBBS) is provided as an example of how to implement the forked database-specific repository
    -   Update the [app_config.py](./docker/src/py_scripts/lib/app_config.py) file to specify the configuration values for the given web application, comments are defined in the configuration file to describe the configuration variables that should be defined.
    -   Update the [app.py](./docker/src/py_scripts/app.py) to define the web actions to execute for the given web app, to capture the elapsed time for each web action, and log the standard metrics in the defined .csv file.
        -   There is a block comment defined in app.py that indicates where the custom code should be defined for a given web app
    -   Update the bash script deployment configuration file [project_deploy_config.sh](./docker/src/sh_scripts/config/project_deploy_config.sh) to specify the appropriate values:
        -   project_path is the folder name of the working copy of the repository that will be used to build the container
        -   git_url is the project git URL value
    -   Update the [README.md](./README.md) file to change the volume names, document title heading, and setup procedure accordingly
    -   Update the docker compose runtime configuration file [docker-compose.prod.yml](./docker/docker-compose.prod.yml) to specify repository-specific the volume names and container name
    -   Update the docker compose configuration file [docker-compose.yml](./docker/docker-compose.yml) to specify the volume names and image/container names for the forked project
    -   Commit the changes to the forked repository

## Building/Running Container (Standalone Implementation Only)
-   Execute the appropriate build and deploy script for the given scenario (e.g. [build_deploy_project.remote.sh](./deployment_scripts/build_deploy_project.remote.sh) for the remote scenario)

## Docker Application Processing
-   The [app.py](./docker/src/py_scripts/app.py) python script will execute when the container is executed
    -   The script will check the active project_scenario_config.sh file to determine if this is a local, remote, or hybrid scenario.    
        -   The active project_scenario_config.py file will be determined by which docker preparation script is executed (e.g. [project_scenario_config.local.sh](./docker/src/py_scripts/lib/project_scenario_config.local.py) for the [prepare_docker_project.local.sh](./deployment_scripts/prepare_docker_project.local.sh) preparation script)
    -   The python script will open a web browser on the container app to the specified web url:
        -   if the runtime value of app_location is "remote" then the app navigates to the remote_web_url before executing the defined web actions
        -   if the runtime value of app_location is "local" then the app navigates to the local_web_url before executing the defined web actions
    -   Next, the script will execute all of the web actions defined in the [app.py](./docker/src/py_scripts/app.py) python script
         -   The performance metrics will be saved to a comma-delimited file with a name of the csv_output_file variable value defined in [app_config.py](./docker/src/py_scripts/lib/app_config.py) in the data volume (defined in [docker-compose.prod.yml](./docker/docker-compose.prod.yml))
        -   All log messages generated by the container app will be appended to a log file with a name of the log_file_prefix variable value defined in [app_config.py](./docker/src/py_scripts/lib/app_config.py) in the logs volume (defined in [docker-compose.prod.yml](./docker/docker-compose.prod.yml)), the log file name will be appended with the date in YYYYMMDD format with a ".log" file extension.

## Checking Results
-   Open the docker volume web-app-metrics-logs to view the log files for the different executions of the docker container
-   Open the docker volume web-app-metrics-data to view the exported data files for the different queries
    -   Open the file that with a file name defined in the csv_output_file variable value defined in [app_config.py](./docker/src/py_scripts/lib/app_config.py) in the data volume (defined in [docker-compose.prod.yml](./docker/docker-compose.prod.yml)) to view the metrics that were captured for each web action

## Standard Metrics/Information Logging
-   The following metrics and information is captured for each web action in a .csv file:
    -   App Name - The name of the web application being evaluated (defined in the app_name variable defined in [app_config.py](./docker/src/py_scripts/lib/app_config.py))
    -   Metrics App Location - The location of this Web App Metrics docker app the metrics will be captured by (defined in container_location of the active project_scenario_config.py file for the given scenario - e.g. [project_scenario_config.remote.py](./docker/src/py_scripts/lib/project_scenario_config.remote.py) for the remote scenario)
    -   Web App Location - The location of the Web App the metrics will be captured from (defined in app_location of the active project_scenario_config.py file for the given scenario - e.g. [project_scenario_config.remote.py](./docker/src/py_scripts/lib/project_scenario_config.remote.py) for the remote scenario)
    -   Date/Time - The Date/Time the given web action was started in MM/DD/YYYY HH:MI:SS AM/PM format
    -   Page Name - The title tag from the page the web action was executed on
    -   Action - The type of web action
    -   # Files - The total number of web resource files (e.g. image, css, JavaScript file, etc.) downloaded for the given web action
    -   Total File Size (KB) - The total size in kilobytes of the web resource files downloaded for the given web action
    -   Total Response Time (s) - The total number of seconds for the web action to complete and the app is ready to accept user interactions
    -   Screenshot file name - the name of the screenshot file saved in the data volume for the given web action

## Implemented Web Actions
-   \*Note: This depends on the web app that the actions are being executed on, see [WAM - IBBS](https://github.com/noaa-pifsc/PIFSC-Tools-Web-App-Metrics-IBBS) as an example of the web actions that are implemented in the IBBS app

## License
See the [LICENSE.md](./LICENSE.md) for details

## Disclaimer
This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.
