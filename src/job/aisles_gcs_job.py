# from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment

def create_aisle_sink_gcs(t_env):
    table_name = 'aisle_sink'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            `aisle_id` INT,
            `aisle` STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'gs://fake-ecommerce-taxi-data-447320/insta_cart/aisles/',  -- Output GCS path for aisles
            'format' = 'csv',
            'sink.parallelism' = '1'
        )
    """
    t_env.execute_sql(sink_ddl)
    
    return table_name


def create_aisle_source_local(t_env):
    table_name = "aisle_source"
    
    source_ddl = f"""
        CREATE TABLE {table_name} (
            `aisle_id` INT,
            `aisle` STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file:///opt/data/aisles.csv',  -- Local CSV file path for aisles
            'format' = 'csv',
            'csv.ignore-parse-errors' = 'true'
        );
    """
    t_env.execute_sql(source_ddl)
    
    return table_name


def log_processing_aisles():
    # Set up the table environment for batch mode using the unified TableEnvironment
    settings = EnvironmentSettings.new_instance().in_batch_mode().build()
    t_env = TableEnvironment.create(settings)
    
    try:
        # Create source and sink tables
        source_table = create_aisle_source_local(t_env)
        gcs_sink_table = create_aisle_sink_gcs(t_env)

        # Insert records into the GCS sink
        t_env.execute_sql(
            f"""
            INSERT INTO {gcs_sink_table}
            SELECT
                `aisle_id`,
                `aisle`
            FROM {source_table}
            """
        ).wait()

    except Exception as e:
        print("Writing records to GCS failed:", str(e))


if __name__ == '__main__':
    log_processing_aisles()
