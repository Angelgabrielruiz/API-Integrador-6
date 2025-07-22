from fastapi import APIRouter, Depends, HTTPException, status
from app.infraestructure.schemas.valvula_schema import ValvulaRequest, ValvulaResponse
from app.application.useCase.contenedor_usecase import ContenedorUseCase
from app.dependencies import get_contenedor_use_case
import paho.mqtt.client as mqtt
import json
import os

router = APIRouter()

# Configuración MQTT
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "50.19.13.195")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))

@router.post("/dispensar", response_model=ValvulaResponse)
def solicitar_dispensado_valvula(
    valvula_request: ValvulaRequest,
    use_case: ContenedorUseCase = Depends(get_contenedor_use_case)
):
    """
    Endpoint para solicitar el dispensado a través de válvulas.
    Envía comando MQTT al ESP32/Raspberry y espera confirmación.
    """
    try:
        # Verificar que el contenedor existe y tiene suficiente cantidad
        contenedor = use_case.get_contenedor_by_maquina_and_producto(
            valvula_request.id_maquina, 
            valvula_request.id_producto
        )
        
        if not contenedor:
            raise HTTPException(
                status_code=404, 
                detail="Contenedor no encontrado para esa máquina y producto"
            )
        
        if contenedor.cantidad_actual < valvula_request.cantidad_solicitada:
            raise HTTPException(
                status_code=400, 
                detail="Cantidad insuficiente en el contenedor"
            )
        
        # Enviar comando MQTT al ESP32/Raspberry
        mqtt_topic = f"/maquina/{valvula_request.id_maquina}/valvula/{valvula_request.pin_valvula}/comando"
        mqtt_payload = {
            "accion": "dispensar",
            "cantidad": valvula_request.cantidad_solicitada,
            "id_producto": valvula_request.id_producto,
            "pin_valvula": valvula_request.pin_valvula
        }
        
        # Enviar mensaje MQTT
        client = mqtt.Client()
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
        client.publish(mqtt_topic, json.dumps(mqtt_payload))
        client.disconnect()
        
        return ValvulaResponse(
            id_maquina=valvula_request.id_maquina,
            id_producto=valvula_request.id_producto,
            pin_valvula=valvula_request.pin_valvula,
            cantidad_dispensada=0,  # Se actualizará cuando llegue la confirmación
            estado="comando_enviado"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar solicitud: {str(e)}")

@router.post("/confirmar-dispensado")
def confirmar_dispensado_valvula(
    confirmacion: dict,  # Vendrá del consumer MQTT
    use_case: ContenedorUseCase = Depends(get_contenedor_use_case)
):
    """
    Endpoint interno para confirmar que el dispensado se completó.
    Este será llamado por el consumer cuando reciba la confirmación del ESP32.
    """
    # Este endpoint será usado internamente por el consumer
    pass