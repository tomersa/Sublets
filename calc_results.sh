#!/bin/sh
echo "Prices found on $(for file in $(ls output/analyzed/); do cat output/analyzed/$file; echo ""; done | grep -v None | wc -l) messages"

echo "Prices not found on $(for file in $(ls output/analyzed); do cat output/analyzed/$file; echo ""; done | grep None | wc -l) messages."
