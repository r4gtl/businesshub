#!/bin/bash
set -e

# Modifica pg_hba.conf per permettere accesso dalla rete
cat > "$PGDATA/pg_hba.conf" << EOF
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
host    all             all             0.0.0.0/0               md5
EOF

# Configura postgresql.conf per ascoltare su tutti gli indirizzi
echo "listen_addresses='*'" >> "$PGDATA/postgresql.conf"