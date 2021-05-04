#!/usr/bin/env bash

urlencode() {
    # urlencode <string>
    # Chris Down https://gist.github.com/cdown/1163649

    local length="${#1}"
    for (( i = 0; i < length; i++ )); do
        local c="${1:i:1}"
        case $c in
            [a-zA-Z0-9.~_-]) printf "$c" ;;
            *) printf '%s' "$c" | xxd -p -c1 |
                   while read c; do printf '%%%s' "$c"; done ;;
        esac
    done
}

# https://nuxeo.cdlib.org/nuxeo/authentication/token?applicationName=API+ACCESS&deviceId=&deviceDescription=&permission=rw
deviceId=$(hostname)
applicationName='CDL_API_ACCESS'
echo "device description (what machine is this key for?)"
read device
deviceDescription=$(urlencode "$device")
echo "permission"
select permission in r rw;
do
  if [[ $permission ]]; then
    break
  fi
done
echo "https://nuxeo.cdlib.org/nuxeo/authentication/token?applicationName=$applicationName&deviceId=$deviceId&deviceDescription=$deviceDescription&permission=$permission"