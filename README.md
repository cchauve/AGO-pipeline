# SPP-DCJ Pipeline
### Evan Cribbie, Cedric Chauve.

## Data

```python3 scripts/import_YGOB_data.py > log/YGOB_test1/import_data.log```  

Families were labeled from 1 increasingly.
Family `352` was renamed `10352` for robustness checking.
Family `353` was renamed `353a` for the same purpose.  

This script imports already filtered data from Evan's
directory. Ideally we should have two scripts to (1) import data from
the YGOB website and generates statistics and (2) filter data from
users choices.  

The first script should be parameterized by an optional list of
species and download only data files for the selected species and
filter the species tree to include only the considered species.  

The second script shoud be parameterized by a min/max thresholds for
the size of gene families. It would then filter gene families to the
ones not in the size range.  

## Pipeline

The parameters file is `parameters/YGOB_test1_NT.yml`. As I had spaces issues,
I have set the output directories (log and results) in
`/scratch/chauvec/SPP`.  

```
source AGO_python3/bin/activate
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml init
wc -l /scratch/chauvec/SPP/YGOB_test1_NT/aux/families.txt
5028 /scratch/chauvec/SPP/YGOB_test1_NT/aux/families.txt
```

We start with 5028 families.  

### MACSE

```
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml run_macse y
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml check_macse y
```

Log and error files are available at `/scratch/chauvec/SPP/YGOB_test1_NT/log/YGOB_test1_NT_MACSE.[log,err]`.  

We run MACSE on the families that failed, increasing the time limit to
1:00:00 per family.

```
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml rerun_macse 4G 1:00:00 y
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml check_macse y
```

Log and error files are available at `/scratch/chauvec/SPP/YGOB_test1_NT/log/YGOB_test1_NT_MACSE.[log,err]`.  
```
grep -c ">" /scratch/chauvec/SPP/YGOB_test1_NT/log/YGOB_test1_NT_MACSE.err
47
```

There are 47 families that were not aligned due to the time limit, but
for family 2231 (unidentified error). We leave it as is to test the
robustness of the pipeline to intermediate computations failing on
some families.  

We end the MACSE phase by updating the list of active families to
discard the ones for which MACSE failed to complete.

```
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml update_post_macse pre_MACSE
wc -l /scratch/chauvec/SPP/YGOB_test1_NT/aux/families.txt
4981 /scratch/chauvec/SPP/YGOB_test1_NT/aux/families.txt
wc -l /scratch/chauvec/SPP/YGOB_test1_NT/aux/families.txt_pre_MACSE
5028 /scratch/chauvec/SPP/YGOB_test1_NT/aux/families.txt_pre_MACSE
```

We now have 4981 families. 

### GeneRax

```
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml aux_generax
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml run_generax y
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml check_generax y
```

Log and error files are available at `/scratch/chauvec/SPP/YGOB_test1_NT/log/YGOB_test1_NT_GeneRax.[log,err]`.
```
grep -c ">" /scratch/chauvec/SPP/YGOB_test1_NT/log/YGOB_test1_NT_GeneRax.err
187
```

There are 187 families for which GeneRax could not read the alignment.
We update the active families and species tree.

```
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml update_post_generax pre_GeneRax
wc -l /scratch/chauvec/SPP/YGOB_test1_NT/aux/families.txt
4794 /scratch/chauvec/SPP/YGOB_test1_NT/aux/families.txt
```

We now have 4794 families.  

We convert the reconciled trees in recPhyloXML format and compute
statistics for each tree.

```
source AGO_python2/bin/activate
python AGO_pipeline_p2.py parameters/YGOB_test1_NT.yml postprocess_generax
deactivate
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml stats_generax
```

We can observe again a gene content inflation in reconciled gene trees 
obtained with GeneRax.  


### DeCoSTAR

```
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml aux_decostar
python3 AGO_pipeline.py parameters/YGOB_test1_NT.yml run_decostar y
```
