# Taller_ICC_2025
Repo del Taller ICC 2025

## Attack & Defense

Para el server:
```bash
    nano /etc/systemd/system/chall.service  # Aqui poner la configuracion del service

    sudo systemctl daemon-reexec       # si hiciste cambios recientes
    sudo systemctl daemon-reload       # para cargar el nuevo .service
    sudo systemctl enable chall.service
    sudo systemctl start chall.service
```

Para Shovel & Suricata:

```bash
    git clone https://github.com/FCSC-FR/shovel.git
    cd shovel
    cp example.env .env
    docker-compose up		
```

Desde una terminal ssh: ssh ctf@server_ip -L 8000:127.0.0.1:8000

Esto para el .env:
```bash
    CTF_START_DATE=2025-05-31T13:00+00:00
    CTF_TICK_LENGTH=180
    CTF_SERVICES=taller_icc_1
    CTF_SERVICE_TALLER_ICC_1=192.168.159.132:5000
```

Configuración del docker:

```bash
# Copyright (C) 2024  ANSSI
# SPDX-License-Identifier: C0-1.0
services:
  suricata:
    build: ./suricata
    image: anssi/shovel-suricata:dev
    volumes:
      - "./input_pcaps:/input_pcaps:ro"
      - "./suricata/rules:/suricata/rules:ro"
      - "./suricata/output:/suricata/output:rw"

    # Mode A: pcap replay mode (slower, for archives replay or rootless CTF)
    # Add `--pcap-file-continuous` to watch for new pcap in folder.
    #command: --pcap-file-continuous -r /input_pcaps

    # Mode B: capture interface (fast, requires root on vulnbox and in Docker)
    # Drastically reduces ingest delay, but requires to setup traffic mirroring
    # between the vulnbox game interface and a team server.
    command: -i ens33
    cap_add:
      - NET_ADMIN
    network_mode: "host"

    # Mode C: PCAP-over-IP (fast, requires root on vulnbox)
    # Connects to a PCAP-over-IP server, such as pcap-broker to read PCAP data.
    #command: -r /dev/stdin
    #restart: always
    #depends_on:
    #  - pcap-broker
    #environment:
    #  - PCAP_OVER_IP=pcap-broker:4242

  webapp:
    build: ./webapp
    image: anssi/shovel-webapp:dev
    restart: always
    volumes:
      # You may remove the next line to prevent users from downloading pcaps.
      - "./input_pcaps:/input_pcaps:ro"
      # Write access is required in SQLite `mode=ro` as readers need to record
      # a mark in the WAL file. If you need to make the volume read-only, then
      # use `immutable=1` parameter in SQLite databases URI. In immutable mode,
      # SQLite doesn't follow changes made to the database.
      - "./suricata/output:/suricata/output:rw"
    ports:
      - 127.0.0.1:8000:8000
    env_file:
      - .env

  #pcap-broker:
  #  container_name: pcap-broker
  #  build:
  #    context: .
  #    dockerfile_inline: |
  #      FROM golang:alpine
  #      RUN apk add --no-cache build-base libpcap-dev openssh-client tcpdump
  #      RUN go install github.com/fox-it/pcap-broker@latest
  #      ENTRYPOINT ["pcap-broker"]
  #  restart: always
  #  volumes:
  #    - "~/.ssh/id_ed25519:/root/.ssh/id_ed25519:ro"
  #  environment:
  #    PCAP_COMMAND: |-
  #        ssh root@vulnbox -oStrictHostKeyChecking=no
  #        tcpdump -U --immediate-mode -ni game -s 65535 -w - not tcp port 22
  #    LISTEN_ADDRESS: 0.0.0.0:4242
```