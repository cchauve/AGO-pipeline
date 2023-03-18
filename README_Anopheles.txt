
Sat Mar 18 09:16:35 PDT 2023

The parameters file is `parameters/Anopheles_GeneRax_NT.yaml`.
The output root directory is `/scratch/chauvec/SPP`.

```
> source AGO_python3/bin/activate
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml init
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families.txt
```

### MACSE

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script MACSE
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/MACSE/MACSE.sh
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check MACSE
```
```
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/MACSE.log
```

### GeneRax

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script GeneRax
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/GeneRax/GeneRax.sh
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check GeneRax
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats GeneRax
```
```
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/GeneRax.log
```
```
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations.txt
```

### DeCoSTAR

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script DeCoSTAR
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/DeCoSTAR/DeCoSTAR.sh
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check DeCoSTAR
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats DeCoSTAR
```

### SPPDCJ

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script SPPDCJ_ILP
> sbatch  /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/SPPDCJ_ILP_all_species.sh
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check SPPDCJ_ILP
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_ILP_all_species.log
```
```
>python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats SPPDCJ_ILP
```
```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script SPPDCJ
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ/SPPDCJ_all_species.sh
```
