# ==== BASE: Playwright + Python ====

FROM mcr.microsoft.com/playwright/python\:v1.39.0-focal

# ==== Dependências do Sistema Operacional ====

RUN apt-get update && apt-get install -y&#x20;
wget curl unzip gnupg xvfb x11vnc x11-utils xauth dbus&#x20;
supervisor netcat-traditional net-tools procps git&#x20;
libgconf-2-4 libnss3 libnspr4 libasound2 libatk1.0-0 libatk-bridge2.0-0&#x20;
libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 libxcomposite1 libxdamage1&#x20;
libxfixes3 libxrandr2 libxss1 libx11-xcb1 libxext6 libxtst6&#x20;
libpci3 libxrender1 libgdk-pixbuf2.0-0 libpangocairo-1.0-0&#x20;
libharfbuzz-icu0 libsecret-1-0 libenchant-2-2 libmanette-0.2-0&#x20;
libgraphene-1.0-0 libgles2 fonts-liberation fonts-dejavu-core&#x20;
fonts-dejavu-extra fontconfig &&&#x20;
rm -rf /var/lib/apt/lists/\*

# ==== Instala Node.js 18 LTS ====

RUN curl -fsSL [https://deb.nodesource.com/setup\_18.x](https://deb.nodesource.com/setup_18.x) | bash - &&&#x20;
apt-get install -y nodejs && npm install -g npm

# ==== Instala noVNC ====

RUN git clone [https://github.com/novnc/noVNC.git](https://github.com/novnc/noVNC.git) /opt/novnc &&&#x20;
git clone [https://github.com/novnc/websockify](https://github.com/novnc/websockify) /opt/novnc/utils/websockify &&&#x20;
ln -s /opt/novnc/vnc.html /opt/novnc/index.html

# ==== Diretório principal da aplicação ====

WORKDIR /app
COPY . /app

# ==== Instala Rust (necessário para compilar algumas libs como tokenizers) ====

RUN apt-get update &&&#x20;
apt-get install -y curl build-essential &&&#x20;
curl [https://sh.rustup.rs](https://sh.rustup.rs) -sSf | sh -s -- -y &&&#x20;
. "\$HOME/.cargo/env"

# ==== Instala dependências Python principais ====

RUN pip install --upgrade pip &&&#x20;
pip install --no-cache-dir&#x20;
playwright==1.39.0&#x20;
selenium==4.27.1&#x20;
fastapi==0.115.1&#x20;
uvicorn==0.23.2&#x20;
requests==2.32.2&#x20;
aiofiles==23.2.1&#x20;
python-multipart==0.0.9&#x20;
discord.py==2.3.2&#x20;
chromedriver-autoinstaller==0.6.4&#x20;
watchdog==3.0.0&#x20;
langchain-mistralai==0.2.10&#x20;
pyperclip==1.9.0&#x20;
gradio==4.44.1&#x20;
json-repair==0.42.0&#x20;
MainContentExtractor==0.0.4&#x20;
transformers==4.51.3&#x20;
torch==2.7.0&#x20;
accelerate==1.6.0&#x20;
huggingface-hub==0.30.2

# ==== Instala browser-use diretamente ====

RUN pip install browser-use

# ==== Configura Supervisor para gerenciar múltiplos serviços ====

RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# ==== Variáveis de Ambiente Globais ====

ENV PYTHONUNBUFFERED=1&#x20;
BROWSER\_USE\_LOGGING\_LEVEL=info&#x20;
DISPLAY=:99&#x20;
RESOLUTION=1920x1080x24&#x20;
VNC\_PASSWORD=vncpassword&#x20;
CHROME\_PERSISTENT\_SESSION=true&#x20;
RESOLUTION\_WIDTH=1920&#x20;
RESOLUTION\_HEIGHT=1080&#x20;
PLAYWRIGHT\_BROWSERS\_PATH=/mnt/data/ms-playwright&#x20;
CHROME\_PATH=/mnt/data/ms-playwright/chromium-\*/chrome-linux/chrome&#x20;
PORT=10000

# ==== Portas expostas ====

EXPOSE 10000 7788 6080 5901

# ==== Comando de inicialização (executa múltiplos serviços) ====

CMD \["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
