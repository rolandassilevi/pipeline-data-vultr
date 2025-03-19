WITH inverter AS (
    SELECT
        TIMESTAMP,
        DATE,
        ANNEE,
        MOIS,
        JOUR,
        HEURE,
        PV1,
        PV2,
        PV3,
        PV4,
        PV5,
        PV6,
        PV7,
        PV8,
        PV9,
        PV10,
        MPPT1A,
        MPPT2A,
        MPPT3A,
        MPPT4A,
        MPPT5A,
        MPPT1V,
        MPPT2V,
        MPPT3V,
        MPPT4V,
        MPPT5V,
        PHASE_A_CURRENT,
        PHASE_B_CURRENT,
        PHASE_C_CURRENT,
        PHASE_A_VOLTAGE,
        PHASE_B_VOLTAGE,
        PHASE_C_VOLTAGE,
        TOTAL_DC_POWER,
        TOTAL_ACTIVE_POWER,
        DAILY_YIELD,
        TOTAL_YIELD
    FROM {{ source('public', 'inverter_data') }}
)

SELECT * FROM inverter;

--Crée une vue normalisée stg_inverter_data.
