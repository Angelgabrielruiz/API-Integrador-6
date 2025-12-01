from app.domain.repositories.sensor_reading_repository import ISensorReadingRepository
from app.domain.entities.sensor_reading import SensorReading
from app.infrastructure.schemas.sensor_reading_schema import SensorReadingCreate

class SensorUseCase:
    def __init__(self, sensor_reading_repository: ISensorReadingRepository):
        self.sensor_reading_repository = sensor_reading_repository

    def create_sensor_reading(self, sensor_reading_data: SensorReadingCreate) -> SensorReading:
        sensor_reading = SensorReading(
            machine_id=sensor_reading_data.machine_id,
            sensor_type=sensor_reading_data.sensor_type,
            value_numeric=sensor_reading_data.value_numeric,
            unit=sensor_reading_data.unit
        )
        return self.sensor_reading_repository.save(sensor_reading)

    def get_all_sensor_readings(self):
        return self.sensor_reading_repository.find_all()
    
    # NUEVO: Método para eliminar sensores de moneda
    def delete_coin_sensors(self) -> int:
        """Elimina todos los registros de sensores de tipo 'moneda'"""
        deleted_count = self.sensor_reading_repository.delete_by_sensor_type("moneda")
        return deleted_count
    
    # NUEVO: Método genérico para eliminar por tipo de sensor
    def delete_sensors_by_type(self, sensor_type: str) -> int:
        """Elimina todos los registros de sensores del tipo especificado"""
        deleted_count = self.sensor_reading_repository.delete_by_sensor_type(sensor_type)
        return deleted_count