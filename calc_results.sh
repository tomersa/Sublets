echo "Found:$(for file in $(ls output/analyzed/); do cat output/analyzed/$file; echo ""; done | grep -v None | wc -l)"

echo "None:$(for file in $(ls output/analyzed); do cat output/analyzed/$file; echo ""; done | grep None | wc -l)"
