FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# Fix Kali GPG Keys
RUN apt-get update --allow-insecure-repositories && \
    apt-get install -y --no-install-recommends --allow-unauthenticated kali-archive-keyring && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Core system + Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-dev \
        curl wget git ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install kali-linux-headless (brings most pentesting tools + dependencies)
# This includes: nmap, nikto, dirb, gobuster, sqlmap, netcat, ssh, etc.
RUN apt-get update && \
    echo "console-setup console-setup/variant select Latin1 and Latin5 - western Europe and Turkic languages" | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        kali-linux-headless \
        seclists \
        burpsuite \
        default-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Metasploit
 RUN curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > /tmp/msfinstall && \
     chmod 755 /tmp/msfinstall && \
     /tmp/msfinstall && \
     rm /tmp/msfinstall

# FIX: pip system-packages warning
RUN mkdir -p /root/.pip && \
    echo "[global]" > /root/.pip/pip.conf && \
    echo "break-system-packages = true" >> /root/.pip/pip.conf



WORKDIR /opt/cybersentry

# Install cybersentry 
RUN pip3 install  --ignore-installed cybersentry-framework

# .env Template (overwritten if .env file present in logs)
RUN echo 'OPENAI_API_KEY="sk-1234"' > /opt/cybersentry/.env && \
    echo 'ANTHROPIC_API_KEY=""' >> /opt/cybersentry/.env && \
    echo 'DEEPSEEK_API_KEY=""' >> /opt/cybersentry/.env && \
    echo 'OLLAMA_API_BASE=""' >> /opt/cybersentry/.env && \
    echo 'PROMPT_TOOLKIT_NO_CPR=1' >> /opt/cybersentry/.env && \
    echo 'cybersentry_STREAM=false' >> /opt/cybersentry/.env

#  logs directory
RUN mkdir -p /opt/cybersentry/logs

# Startup Script
RUN echo '#!/bin/bash' > /opt/cybersentry/start.sh && \
    echo 'if [ -f /config/.env ]; then' >> /opt/cybersentry/start.sh && \
    echo '  echo "Loading .env from /config/.env"' >> /opt/cybersentry/start.sh && \
    echo '  cp /config/.env /opt/cybersentry/.env' >> /opt/cybersentry/start.sh && \
    echo 'fi' >> /opt/cybersentry/start.sh && \
    echo 'cd /opt/cybersentry' >> /opt/cybersentry/start.sh && \
    echo 'exec cybersentry "$@"' >> /opt/cybersentry/start.sh && \
    chmod +x /opt/cybersentry/start.sh

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import cybersentry; print('OK')" || exit 1

ENTRYPOINT ["/opt/cybersentry/start.sh"]
CMD []