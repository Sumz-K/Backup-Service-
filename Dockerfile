FROM ubuntu:latest
WORKDIR /app
COPY . /app
RUN mkdir /app/tokens
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    firefox \
    libgl1-mesa-glx \
    libxcb-dri3-0 \
    libxshmfence-dev \
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0
RUN apt-get update && apt-get install -y firefox \
    libgl1-mesa-glx \
    libxcb-dri3-0 \
    libxshmfence-dev \
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0
RUN pip3 install --no-cache-dir -r requirements.txt
RUN mkdir -p /usr/lib/firefox
ENV DISPLAY=:0
ENV BROWSER=firefox
CMD ["python3","scripts/full_script.py"]
