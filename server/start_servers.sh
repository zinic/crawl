#!/bin/bash
set -euo pipefail
IFS=$'\n\t'


rm -f nginx.log
sudo nginx -p "$(pwd)" -c "nginx.conf"