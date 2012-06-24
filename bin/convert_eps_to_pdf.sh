PATH=/usr/local/bin/:$PATH

for f in "$@"
do
	dir=$(dirname "$f")
   	name=$(basename "$f")
   	base=${name%.*}
	out="$dir/$base.pdf"
	convert -density 300 "$f" "$out"
done