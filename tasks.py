import invoke
import boto3


def list_crawler_names():
    client = boto3.client('glue')
    response = client.list_crawlers(MaxResults=100, Tags={"glue-crawler-experiment": ""})
    return response['CrawlerNames']


def start_crawler(name):
    client = boto3.client('glue')
    client.start_crawler(Name=name)


def get_database_generated_by(crawler_name):
    client = boto3.client('glue')
    return client.get_crawler(Name=crawler_name)['Crawler']['DatabaseName']


def show_table_of_crawler(name):
    client = boto3.client('glue')

    database_name = get_database_generated_by(name)

    print('Database:', database_name)

    tables = client.get_tables(DatabaseName=database_name)
    for table in tables['TableList']:
        print('Table:', table['Name'])
        for partition in table['PartitionKeys']:
            print('Partition:', partition)
        for column in table['StorageDescriptor']['Columns']:
            print('Column:', column)

    print('')


@invoke.task
def list_crawlers(c):
    print(list_crawler_names())


@invoke.task
def start_crawlers(c):
    for crawler in list_crawler_names():
        print('Start crawler:', crawler)
        start_crawler(crawler)


@invoke.task
def show_crawlers_state(c):
    client = boto3.client('glue')
    for crawler in list_crawler_names():
        response = client.get_crawler(Name=crawler)
        print(f'Crawler "{crawler}": {response["Crawler"]["State"]}')


@invoke.task
def show_tables(c):
    for crawler in list_crawler_names():
        show_table_of_crawler(crawler)


@invoke.task
def delete_databases(c):
    client = boto3.client('glue')
    for crawler in list_crawler_names():
        database = get_database_generated_by(crawler)
        print('Delete:', database)
        client.delete_database(Name=database)
