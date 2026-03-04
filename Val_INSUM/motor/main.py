from orquestador import OrquestadorInsumo

if __name__ == "__main__":

    motor = OrquestadorInsumo(
        id_insumo=1,
        ruta_db="config.duckdb"
    )

    motor.procesar()
