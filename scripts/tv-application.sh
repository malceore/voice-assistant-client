#!/bin/bash
set -e

JWT="eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjUzNmY2NmJhLTJlN2MtNDE1NC1iNWNkLTljZGM4YWRkNDIwMyJ9.eyJyb2xlIjoidXNlcl90b2tlbiIsImlhdCI6MTU2MTIzMDM0MiwiaXNzIjoiTm90IHNldC4ifQ.7-Jvr2_qusdlTGAqAgYtb72d1fRuz1oRQmT2zC9Pv0VcRF7e_Lvp8ysk_pxfPBJCeVeO04AQmDH3q9qTEZhbkA"
URL="http://195.168.1.100:8080"
THING="lg-tv-38:8c:50:59:24:df"
APPLICATION="$1"
# Check if tv is on, if not will need to be.
value=$(curl -H "Authorization:Bearer ${JWT}" -H "Content-Type: application/json" -H "Accept: application/json" --insecure --silent ${URL}/things/${THING}/properties | jq .on)
#echo "$value"

if [ "$value" = "false" ]; then
    curl -H "Authorization:Bearer ${JWT}" -H "Content-Type: application/json" -H "Accept: application/json" -X PUT -d '{"'on'":'true'}' --insecure --silent ${URL}/things/${THING}/properties/on
fi
curl -H "Authorization:Bearer ${JWT}" -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d '{"'launchApp'":{"'input'":"'$APPLICATION'"}}' --insecure --silent ${URL}/things/${THING}/actions/launchApp >> /dev/null


