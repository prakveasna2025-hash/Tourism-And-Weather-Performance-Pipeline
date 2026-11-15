# How to Run Airflow Init
docker compose up airflow-init

# start the airflow stack
docker compose up -d

# How to check airflow list(if forget the airflow password!)
 docker compose exec airflow-webserver airflow users list

# always befor went to bed:
docker compose down

# Check connection database by using Airflow's PostgresHook:
docker compose exec airflow-webserver python -c "
from airflow.providers.postgres.hooks.postgres import PostgresHook
try:
    hook = PostgresHook(postgres_conn_id='postgres_warehouse')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    print('✅ CONNECTION SUCCESSFUL!')
    print(f'PostgreSQL version: {cursor.fetchone()[0]}')
    cursor.close()
    conn.close()
except Exception as e:
    print(f'❌ CONNECTION FAILED: {e}')
"

