#!/usr/bin/sh
cd -P -- "$(dirname -- "$0")"

curl 'https://dbd.tricky.lol/api/perks' -o 'perks.json'
curl 'https://dbd.tricky.lol/api/characters' -o 'characters.json'
