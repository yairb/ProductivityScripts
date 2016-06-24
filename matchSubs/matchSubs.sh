#!/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

TARGET_DIR=${1:-`pwd`}
cd $TARGET_DIR
i=0
subs=()
videos=()

function toLowerCase {
	echo "$1" | tr '[:upper:]' '[:lower:]'
}

#iterate recursively through all files in directory
function getSubfiles {
	for x in "$1"/* ; do
		if [[ "$x" =~ \.srt$ ]]; then
			subs+=("$x")
		fi
		if [[ "$x" =~ \.mp4$|\.avi$|\.mkv$ ]]; then
			videos+=("$x")
		fi
    		if [ -d "$x" ]; then
			getSubfiles $x
		fi
		if [[ "$x" =~ \.zip$ ]]; then
			echo "ZIP file!"
			dirName=${x%.*}
			echo "dirName: $dirName"
			unzip -o $x -d $dirName
			rm $x
			getSubfiles $dirName
		fi 
	done
} 

#return sub (with path) to three args: season, episode, version.
# version is optional - if null it'll return the first.
function findSub {
	season=$1
	episode=$2
	version=$3
	for sub in "${subs[@]}" ; do
		subLowerCase=$(toLowerCase $sub)
		if [[ $sub =~ $season[Eex]$episode ]] && [[ $subLowerCase =~ $version ]]; then
			echo $sub
			break
		fi	
	done	
}
echo "******************************************"
echo "Matching subs (2016). Written by Yair"
echo "******************************************"
echo "Target directory: $TARGET_DIR"
getSubfiles $TARGET_DIR

echo "Found ${#videos[@]} videos, ${#subs[@]} subtitles"
echo "Starting the matching..."
counter=0
for vid in "${videos[@]}" ; do
	echo "video name: ${vid##*/}"
	vidLower=$(toLowerCase $vid)
	version=''
	if [[ "$vidLower" =~ lol|evolve|killers|asap|avs|fum|batv|fleet|sva|dimension|skgtv ]]; then
		version=${BASH_REMATCH[0]}
	fi
	if [[ $vid =~ [Ss][0-9]{2}([Ee][0-9]{2})+ ]]; then
		matched=${BASH_REMATCH[0]}
		season=${matched:1:2}
		episode=${matched:4:2}
	elif [[ $vid =~ [0-9]{3} ]]; then
		matched=${BASH_REMATCH[0]}
		season=${matched:0:1}
		episode=${matched:1:2}
		matched=${season}E${episode}
	fi

	if [ -z "$season" ] || [ -z "$episode" ]; then
		echo "Couldn't find season or episode for this video."
		continue
	fi
	fileType=${vid##*.}
	name=${vid%?$matched*}
	name=${name##*/}
	#echo "show name: $name season: $((10#${season})) episode $episode version: $version type: $fileType"
		
	sub=$(findSub $((10#${season})) $episode $version)
	if [ -z "$sub" ]; then
		echo "Didn't find sub"
	else	
		echo "Sub found: ${sub##*/}"
		newName="${TARGET_DIR}/${name}.$matched-${version}"
		if ! [ -e $newName.$fileType ]; then
			mv $vid $newName.$fileType
		fi
		if ! [ -e $newName.srt ]; then
			mv $sub $newName.srt
		fi
		counter=$((counter + 1))
	fi
done

echo "Finished - succeeded matching subs for $counter videos"
IFS=$SAVEIFS
