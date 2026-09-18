import numpy as np
import joblib
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

class TrainModel:

    def entrenarModelo():

        load_dotenv("/app/.env")
        USER = os.getenv("SUPABASE_USER")
        PASSWORD = os.getenv("SUPABASE_PASSWORD")
        HOST = os.getenv("SUPABASE_HOST")
        PORT = os.getenv("SUPABASE_PORT")
        DBNAME = os.getenv("SUPABASE_DBNAME")

        if PORT is None:
            print("no se lee el env")
            return
        else:
            print("si se lee en env")

        try:
            with psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                dbname=DBNAME
            ) as connection:
                with connection.cursor() as cursor:
                    # La vista ya trae pais, ciudad, tipo_correo y genero_musical por cliente
                    cursor.execute('SELECT tipo_correo, pais, ciudad, genero_musical FROM vw_cliente_genero;')
                    rows = cursor.fetchall()
                    print(f"Filas recuperadas: {len(rows)}")

        except Exception as e:
            print(f"Error al conectar o recuperar datos: {e}")
            return

        if not rows:
            print("No se recuperaron filas de la base de datos. Abortando entrenamiento.")
            return
        else:
            print(rows[:2])

        # Convertir a DataFrame
        df = pd.DataFrame(rows, columns=["tipo_correo", "pais", "ciudad", "genero_musical"])

        X = df[["pais", "ciudad", "tipo_correo"]]
        y_raw = df["genero_musical"]

        # Codificar la etiqueta (genero_musical) a numeros
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y_raw)

        # Codificar features categoricas con OneHotEncoder dentro de un pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), ["pais", "ciudad", "tipo_correo"])
            ]
        )

        modelo_pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=200, random_state=42))
        ])

        # Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if len(set(y)) > 1 else None
        )

        # Entrenar
        modelo_pipeline.fit(X_train, y_train)

        # Evaluar
        y_pred = modelo_pipeline.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

        # Guardar modelo y el label encoder
        joblib.dump(modelo_pipeline, str(os.getenv("MODELO_ENTRENADO")))
        joblib.dump(label_encoder, str(os.getenv("MODELO_ENTRENADO")).replace(".pkl", "_label_encoder.pkl"))
        print("modelo entrenado")
