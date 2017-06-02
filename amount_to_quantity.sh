if [[ -z "$1" ]]; then ending='*.*'; else ending="*.$1"; fi

find ./ -type f -iname "$ending" -exec sed -i -e 's/amount/quantity/g' {} \;
find ./ -type f -iname "$ending" -exec sed -i -e 's/Amount/Quantity/g' {} \;
find ./ -type f -iname "$ending" -exec sed -i -e 's/AMOUNT/QUANTITY/g' {} \;
