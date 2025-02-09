# Usa la imagen base
FROM python:3.12-slim-bookworm

# Establece el directorio de trabajo
WORKDIR /usr/src/app/workspace

# Actualiza los paquetes e instala dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl sudo nano wget unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia e instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crea los usuarios
ARG JESUS_PASSWORD
ARG IKER_PASSWORD
RUN useradd -ms /bin/bash jesus && \
    echo "jesus:${JESUS_PASSWORD}" | chpasswd && \
    usermod -aG sudo jesus && \
    useradd -ms /bin/bash iker && \
    echo "iker:${IKER_PASSWORD}" | chpasswd && \
    usermod -aG sudo iker

# Permisos sudo sin contraseña
RUN echo "jesus ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "iker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && visudo -c

# Cambia la propiedad de los archivos
RUN chown -R jesus:jesus /usr/src/app/workspace && \
    chown -R iker:iker /usr/src/app/workspace

# Establece el usuario JESUS por defecto
USER jesus

# Establece el comando de inicio
CMD ["python", "/usr/src/app/workspace/main.py"]