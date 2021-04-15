whatis("Name : sparc-dft-api")
whatis("Version : {{ version }}")
whatis("Target : x86_64")
whatis("Short description : sparc-dft-api is an ASE based python wrapper for the density functional theory (DFT) code SPARC.")
help([[sparc-dft-api is an ASE based python wrapper for the density functional theory (DFT) code SPARC.]])
setenv("SPRC_DFT_API_ROOT", "{{ root_path }}") 
prepend_path("PYTHONPATH", "{{ root_path }}")
setenv("SPARC_PSP_PATH", "{{ root_path }}/sparc/pseudos/PBE_pseudos")
if (os.getenv("PBS_NP")) then
  setenv("ASE_SPARC_COMMAND", "mpirun -np $PBS_NP sparc -name PREFIX")
else
  setenv("ASE_SPARC_COMMAND", "mpirun -np 24 sparc -name PREFIX")
end
load("ase/3.19.0")
--prepend_path("MODULEPATH", "/storage/home/hcodaman1/yandeweg3/pace-community-project/SPARC/modules/Core")
--load("SPARC/1.0.0")
