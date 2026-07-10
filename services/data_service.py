VEHICULOS_DEMO = {
    "ABCD12": {
        "cliente": "Cliente de prueba",
        "telefono": "+56900000000",
        "correo": "cliente@email.com",
        "marca": "Toyota",
        "modelo": "Hilux",
        "anio": "2020",
        "patente": "ABCD12",
        "kilometraje": "120000",
        "vin": "VIN-DEMO-123",
    }
}


def normalizar_patente(patente: str) -> str:
    return (patente or "").upper().replace("-", "").replace(" ", "").strip()


def buscar_por_patente(patente: str):
    return VEHICULOS_DEMO.get(normalizar_patente(patente))
