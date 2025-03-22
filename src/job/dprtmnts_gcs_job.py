# from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment

def create_departments_sink_gcs(t_env):
    table_name = 'departments_sink'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            `department_id` INT,
            `department` STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'gs://fake-ecommerce-taxi-data-447320/insta_cart/departments/',  -- Output GCS path for departments
            'format' = 'csv',
            'sink.parallelism' = '1'
        )
    """
    t_env.execute_sql(sink_ddl)
    
    return table_name


def create_departments_source_local(t_env):
    table_name = "departments_source"
    
    source_ddl = f"""
        CREATE TABLE {table_name} (
            `department_id` INT,
            `department` STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file:///opt/data/departments.csv',  -- Local CSV file path for departments
            'format' = 'csv',
            'csv.ignore-parse-errors' = 'true'
        );
    """
    t_env.execute_sql(source_ddl)
    
    return table_name


def log_processing_departments():
    # Set up the table environment for batch mode using the unified TableEnvironment
    settings = EnvironmentSettings.new_instance().in_batch_mode().build()
    t_env = TableEnvironment.create(settings)
    
    try:
        # Create source and sink tables
        source_table = create_departments_source_local(t_env)
        gcs_sink_table = create_departments_sink_gcs(t_env)

        # Insert records into the GCS sink
        t_env.execute_sql(
            f"""
            INSERT INTO {gcs_sink_table}
            SELECT
                `department_id`,
                `department`
            FROM {source_table}
            """
        ).wait()

    except Exception as e:
        print("Writing records to GCS failed:", str(e))


if __name__ == '__main__':
    log_processing_departments()
