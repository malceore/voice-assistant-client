#!/bin/bash
set -e

JWT="eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjUzNmY2NmJhLTJlN2MtNDE1NC1iNWNkLTljZGM4YWRkNDIwMyJ9.eyJyb2xlIjoidXNlcl90b2tlbiIsImlhdCI6MTU2MTIzMDM0MiwiaXNzIjoiTm90IHNldC4ifQ.7-Jvr2_qusdlTGAqAgYtb72d1fRuz1oRQmT2zC9Pv0VcRF7e_Lvp8ysk_pxfPBJCeVeO04AQmDH3q9qTEZhbkA"
URL="http://195.168.1.100:8080"
THING="$1"
PROPERTY="$2"
VALUE="$3"

if [ -z "${VALUE}" ]; then
  echo "Usage: set-property.sh THING PROPERTY VALUE"
  exit 1
fi

curl -H "Authorization:Bearer ${JWT}" \
 -H "Content-Type: application/json" \
 -H "Accept: application/json" \
 -X PUT -d '{"'${PROPERTY}'":'${VALUE}'}' \
 --insecure --silent \
${URL}/things/${THING}/properties/${PROPERTY} > /dev/null
