_self=$(dirname $0)

up=${1:-0}

re='^[0-9]+$'
if ! [[ $up =~ $re ]] || [ -z "$2" ] ; then
  echo "filt_make.sh # tgt"
	echo "  where # is the number of directories up to the code root"
	exit 1
fi

tgt=$2

rm -f /tmp/filt_make_err.dat
make MM=-MM $tgt 2> /tmp/filt_make_err.dat | \
 python ${_self}/filt_deps.py $up Y | sort | uniq
echo "Make Errors"
cat /tmp/filt_make_err.dat

