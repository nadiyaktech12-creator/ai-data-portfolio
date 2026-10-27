import duckdb

con = duckdb.connect("data/iot_fleet.duckdb")

print("=== Daily average temperature by region ===")
print(con.execute("""
    SELECT 
        region,
        DATE_TRUNC('day', timestamp) AS day,
        ROUND(AVG(temperature_c), 2) AS avg_temp,
        ROUND(AVG(humidity_pct), 1) AS avg_humidity,
        SUM(CASE WHEN status = 'offline' THEN 1 ELSE 0 END) AS offline_events
    FROM sensor_telemetry
    GROUP BY 1, 2
    ORDER BY 2, 1
    LIMIT 10
""").df())

con.close()