cd src
sed -i 's/USE_MKL       = 0/USE_MKL       = 1/' makefile
make clean
make
