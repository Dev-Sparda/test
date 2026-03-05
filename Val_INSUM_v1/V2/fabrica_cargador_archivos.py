# fabrica_cargador_archivos.py
import polars as pl
from pathlib import Path


class FabricaCargadorArchivos:
    """
    Fábrica que carga archivos según su tipo
    """
    
    @staticmethod
    def cargar(ruta: str, tipo_archivo: str, hoja: str = None):
        """
        Carga un archivo según el tipo especificado
        
        Args:
            ruta: Ruta al archivo
            tipo_archivo: CSV, TXT o EXCEL
            hoja: Nombre de la hoja (solo para Excel)
        
        Returns:
            pl.LazyFrame: Datos en formato lazy
        """
        # Validar que el archivo existe
        if not Path(ruta).exists():
            raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
        
        if tipo_archivo == "CSV":
            return pl.scan_csv(
                ruta,
                has_header=False,          # Sin encabezados
                infer_schema_length=0,      # No inferir tipos
                low_memory=True              # Modo bajo consumo de memoria
            )
        
        elif tipo_archivo == "TXT":
            return pl.scan_csv(
                ruta,
                separator="\t",              # Tabulador como separador
                has_header=False,
                infer_schema_length=0,
                low_memory=True
            )
        
        elif tipo_archivo == "EXCEL":
            if hoja:
                # Cargar hoja específica
                return (
                    pl.read_excel(
                        ruta,
                        sheet_name=hoja,
                        has_header=False
                    )
                    .lazy()
                )
            else:
                # Cargar primera hoja
                return (
                    pl.read_excel(
                        ruta,
                        has_header=False
                    )
                    .lazy()
                )
        
        else:
            raise ValueError(f"Tipo de archivo no soportado: {tipo_archivo}")
