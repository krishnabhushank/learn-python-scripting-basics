import argparse
import configparser
import logging.config
import sys
import time

import boto3


def has_query_succeeded(athena_client, exec_id):
    state = "RUNNING"
    max_execution = 10

    while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
        max_execution -= 1
        response = athena_client.get_query_execution(QueryExecutionId=exec_id)
        if (
                "QueryExecution" in response
                and "Status" in response["QueryExecution"]
                and "State" in response["QueryExecution"]["Status"]
        ):
            state = response["QueryExecution"]["Status"]["State"]
            if state == "SUCCEEDED":
                statistics = response["QueryExecution"]["Statistics"]
                logger.info(f"Statistics : {statistics}")
                return True
            if state == "FAILED":
                athena_error = response["QueryExecution"]["Status"]["AthenaError"]
                logger.error(f"AthenaError : {athena_error}")
            
        time.sleep(30)

    return False


def execute_query(athena_client, my_workgroup, my_query):
    logger.info("Query")
    print(f'{my_query}')

    response = athena_client.start_query_execution(
        QueryString=f'{my_query}',
        WorkGroup=f'{my_workgroup}', 
        ResultConfiguration={"OutputLocation": result_output_location}
    )
    return response["QueryExecutionId"]


def read_sql_file(file_name):
    with open(file_name) as my_file:
        return my_file.read()


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Connect to AWS Athena and run Hive Queries')
    parser.add_argument('-p', '--params',
                        help='Comma Separated Key=value Parameter List')
    parser.add_argument('-P', '--profile',
                        help='Path to INI/Configuration File',
                        required='True')
    parser.add_argument('-f', '--file',
                        help='Path to SQL File',
                        required='True')

    results = parser.parse_args(args)
    return (results.params,
            results.profile,
            results.file)


if __name__ == '__main__':
    params, profile, file = check_arg(sys.argv[1:])

    lc_configFile = profile
    logging.config.fileConfig(lc_configFile)
    logger = logging.getLogger('generateData')

    logger.info("Using Config from " + str(lc_configFile))

    global config
    config = configparser.ConfigParser()
    config.read(lc_configFile)

    region = config.get('athena_info', 'REGION')
    boto3_athena_client = boto3.client("athena", region_name=region)

    global result_output_location, db_name
    workgroup = config.get('athena_info', 'WORKGROUP')
    result_output_location = config.get('athena_info', 'RESULTS_S3_URL')

    logger.info("Athena ::")
    logger.info(f"Region : {region}")
    logger.info(f"Workgroup : {workgroup}")
    logger.info(f"Output Location for Results : {result_output_location}")

    logger.info("Inputs ::")
    logger.info(f"Param List : {params}")
    logger.info(f"SQL File : {file}")

    # Convert key-value String to dictionary
    # Using map() + split() + loop
    res = []
    for sub in params.split(','):
        if '=' in sub:
            res.append(map(str.strip, sub.split('=', 1)))
    res = dict(res)
    logger.info("The converted dictionary is : " + str(res))

    query = read_sql_file(file)

    for key in res:
        query = query.replace('${'+key+'}', res[key])

    logger.debug(f'Master Query : {query}')

    query_list = query.split(';')
    
    for index, this_query in enumerate(query_list):
      if this_query.isspace() == True:
          continue 

      this_query = this_query.strip()
      count = index + 1
      logger.info(f'------ {count}')
      execution_id = execute_query(athena_client=boto3_athena_client, my_workgroup=workgroup, my_query=this_query)
      logger.info(f'execution_id : {execution_id}')
      query_status = has_query_succeeded(athena_client=boto3_athena_client, exec_id=execution_id)
      logger.info(f"is_query_run_a_success : {query_status}")

      if query_status is True:
          rc = 0
      else:
          rc = 1
          break

    logger.info("Script completed... : " + str(rc))
    sys.exit(rc)


