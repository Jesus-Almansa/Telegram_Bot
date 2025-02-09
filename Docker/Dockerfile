# Usa la imagen base que prefieras
FROM python:3.12-slim-bookworm

# Establece el directorio de trabajo
WORKDIR /usr/src/app/workspace

# Actualiza los paquetes e instala Git y las dependencias necesarias para cv2
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    sudo \
    nano \
    wget \
    unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala las bibliotecas de Python que necesitas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crea el usuario 'JESUS' y 'IKER', utilizando las variables de entorno para las contraseñas
ARG JESUS_PASSWORD
ARG IKER_PASSWORD
RUN useradd -ms /bin/bash jesus && \
    echo "jesus:${JESUS_PASSWORD}" | chpasswd && \
    usermod -aG sudo jesus && \
    useradd -ms /bin/bash iker && \
    echo "iker:${IKER_PASSWORD}" | chpasswd && \
    usermod -aG sudo iker

# Configura que JESUS y iker puedan usar sudo sin contraseña
RUN echo "jesus ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "iker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && visudo -c

# Cambia la propiedad de todos los archivos y directorios de /usr/src/app/workspace a JESUS y iker
RUN chown -R jesus:jesus /usr/src/app/workspace && \
    chown -R iker:iker /usr/src/app/workspace

# Establece el usuario JESUS como el usuario por defecto
USER jesus

# Comando por defecto cuando inicie el contenedor
CMD ["bash", "-c", "cd /usr/src/app/workspace && bash"]
