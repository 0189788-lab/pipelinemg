from pydantic import BaseModel, validator

class PredictorRequest(BaseModel):
    pais: str
    ciudad: str
    tipo_correo: str

    @validator("pais", "ciudad", "tipo_correo")
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("El campo no puede estar vacío")
        return value


