import csv
import sys
import unicodedata
from django.db import transaction
from django.core.exceptions import ValidationError
from oficina.models import Oficina
from persona.models import Persona

def normalizar_email(email):
    if not email:
        return email
    # Elimina acentos y convierte a ASCII
    return unicodedata.normalize('NFKD', email).encode('ascii', 'ignore').decode('ascii')

def run(*args):
    if not args:
        print("Error: Debes indicar la ruta del archivo CSV.")
        return

    csv_file = args[0]

    # Mapeo de oficinas existentes
    oficinas_map = {oficina.nombre_corto.lower(): oficina for oficina in Oficina.objects.all()}

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            personas_a_crear = []

            for row in reader:
                nombre = row.get('nombre')
                apellido = row.get('apellido')
                edad = row.get('edad')
                email = normalizar_email(row.get('email'))
                oficina_nombre_corto = row.get('oficina_nombre_corto')

                # Validación básica
                if not nombre or not apellido or not edad:
                    print(f"Error: Error en fila {row}. Faltan datos obligatorios (nombre, apellido o edad).")
                    continue

                try:
                    edad_int = int(edad)
                except (ValueError, TypeError):
                    print(f"Error: Error en fila {row}. La edad debe ser un número válido.")
                    continue

                oficina_obj = None
                if oficina_nombre_corto:
                    oficina_obj = oficinas_map.get(oficina_nombre_corto.lower())
                    if not oficina_obj:
                        oficina_obj = Oficina(nombre=oficina_nombre_corto, nombre_corto=oficina_nombre_corto)
                        oficina_obj.save()
                        oficinas_map[oficina_nombre_corto.lower()] = oficina_obj
                        print(f"Info: Oficina '{oficina_nombre_corto}' creada automáticamente.")

                try:
                    persona = Persona(
                        nombre=nombre,
                        apellido=apellido,
                        edad=edad_int,
                        email=email,
                        oficina=oficina_obj
                    )
                    persona.full_clean()  # Validación del modelo
                    personas_a_crear.append(persona)
                except ValidationError as e:
                    print(f"Error: Error en fila {row}. {e.message_dict}")
                except Exception as e:
                    print(f"Error: Error en fila {row}. {e}")

        # Guardado masivo
        with transaction.atomic():
            personas = Persona.objects.bulk_create(personas_a_crear)
            print(f"{len(personas)} personas importadas correctamente.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {csv_file}")
    except Exception as e:
        print(f"Error inesperado: {e}")
