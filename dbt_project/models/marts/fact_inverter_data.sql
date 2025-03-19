WITH daily_aggregation AS (
    SELECT
        JOUR,
        SUM(TOTAL_ACTIVE_POWER) AS total_power_generated,
        AVG(PHASE_A_VOLTAGE) AS avg_phase_a_voltage,
        AVG(PHASE_B_VOLTAGE) AS avg_phase_b_voltage,
        AVG(PHASE_C_VOLTAGE) AS avg_phase_c_voltage
    FROM {{ ref('stg_inverter_data') }}
    GROUP BY JOUR
)

SELECT * FROM daily_aggregation;

--Agrège les données par jour.
--Calcule la puissance totale générée.
--Moyenne des tensions des phases.
