#!/bin/bash


s_dir="./images"
list_dir=$(find . -not -path $s_dir -not -path ./.git -mindepth 1 -maxdepth 1 -type d)
list_categories=$(find $s_dir -mindepth 1 -maxdepth 1 -type d)

for dir in $list_categories;
    do
		if [ -d "$dir" ]; then
			prefix=$(basename "$dir" | cut -d'.' -f1 | cut -d'_' -f1);
			echo "Processing: $dir -> $prefix";
			if [ "$prefix" != "$(basename "$dir")" ]; then
				mkdir -p "$prefix";
				npath=$prefix/$(basename "$dir");
				mkdir -p "$npath/Base";
				cp -r "$dir/" "$npath/Base/" && echo "  Moved $dir to $npath/Base";
				mkdir -p "$npath/Augmented" "$npath/Transformed";
			else
				echo "  Skipping $dir (no underscore found)";
			fi;
		fi;
	done