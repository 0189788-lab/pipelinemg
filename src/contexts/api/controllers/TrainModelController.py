import os
import joblib
import pandas as pd

from src.contexts.api.models import PredictorRequest


class TrainModelController:
    def execute(self, request: PredictorRequest):
        print(request)

        pais = request.pais
        ciudad = request.ciudad
        tipo_correo = request.tipo_correo

        # Cargar el pipeline entrenado (preprocesador + clasificador)
        lr_model_path = os.getenv("MODELO_ENTRENADO")
        modelo_cargado = joblib.load(lr_model_path)

        # Cargar el label encoder para poder devolver el nombre del género, no un número
        label_encoder_path = lr_model_path.replace(".pkl", "_label_encoder.pkl")
        label_encoder = joblib.load(label_encoder_path)

        # El pipeline espera un DataFrame con las mismas columnas usadas al entrenar
        nuevo_dato = pd.DataFrame([{
            "pais": pais,
            "ciudad": ciudad,
            "tipo_correo": tipo_correo
        }])

        # Hacer la predicción
        pred_numerica = modelo_cargado.predict(nuevo_dato)
        genero_predicho = label_encoder.inverse_transform(pred_numerica)[0]

        print(f"Predicción para {pais}/{ciudad}/{tipo_correo}: {genero_predicho}")

        return {"status": "OK", "result": genero_predicho}