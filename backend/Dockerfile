# Usa una imagen base ligera de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y los instala
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el código de la aplicación
COPY . /app/

# Expone el puerto en el que correrá la aplicación (8000)
EXPOSE 8000

# Comando para arrancar la aplicación con uvicorn en modo reload para desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
