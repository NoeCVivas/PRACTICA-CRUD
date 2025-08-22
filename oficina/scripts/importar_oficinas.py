import csv
import sys
from django.db import transaction
from django.core.exceptions import ValidationError
from oficina.models import Oficina

def run(*args):
    if not args:
        print("Error: Proporcionar la ruta del archivo")
        print("Uso: python importar_oficinas.py <ruta_del_archivo>")
        sys.exit(1)
    
    
    csv_file = args[0]
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            oficinas_a_crear = []
           
            for row in reader:
                oficina = Oficina
                nombre = row.get('nombre')
                nombre_corto = row.get ('nombre_corto')

                if not row.get('nombre') or not row.get('nombre_corto'):
                    print(f"Error: Faltan datos en la fila {reader.line_num}.")
                    continue
                    
                    
                try:
                    oficina = Oficina(nombre=nombre,
                    nombre_corto=nombre_corto)
                    oficina.full_clean()
                    oficinas_a_crear.append(oficina)
       

                
                except ValidationError as e:
                        print(f"Error de validación en la fila {row}: Detalle: {e}")
                except Exception as e:
                        print(f"Error al crear la oficina en la fila {row}: Detalle: {e}")    
                        continue
                        
                
        
        with transaction.atomic():
            Oficina.objects.bulk_create(oficinas_a_crear)
        print(f"Importadas {len(oficinas_a_crear)} oficinas exitosamente.")


    except FileNotFoundError:
        print(f"Error: El archivo {csv_file} no existe.")
        sys.exit(1)
    except Exception as e:
        print(f"Ocurrio  un error inesperado en la importacion")
   

