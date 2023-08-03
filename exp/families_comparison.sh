echo "## 7 species, all chromosomes"
echo "### OMA.OG versus PO"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families_OG.txt ./proteinortho_20230728/exp_2/families.txt 0
echo '```'
echo "### OMA.OG versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families_OG.txt ../data/VectorBase/families_OG_2.txt 0
echo "### OMA.HOG versus PO"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families_HOG.txt ./proteinortho_20230728/exp_2/families.txt 0
echo '```'
echo "### OMA.HOG versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families_HOG.txt ../data/VectorBase/families_OG_2.txt 0
echo '```'
echo "### PO versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_2/families.txt ../data/VectorBase/families_OG_2.txt 0
echo '```'
echo

echo "## 4 species, all chromosomes"
echo "### OMA.OG versus PO"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families_OG.txt ./proteinortho_20230728/exp_3/families.txt 0
echo '```'
echo "### OMA.OG versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families_OG.txt ../data/VectorBase/families_OG_3.txt 0
echo '```'
echo "### OMA.HOG versus PO"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families_HOG.txt ./proteinortho_20230728/exp_3/families.txt 0
echo '```'
echo "### OMA.HOG versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families_HOG.txt ../data/VectorBase/families_OG_3.txt 0
echo '```'
echo "### PO versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_3/families.txt ../data/VectorBase/families_OG_3.txt 0
echo '```'
echo

echo "## 4 species, X chromosome"
echo "### OMA.OG versus PO"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_4/families_OG.txt ./proteinortho_20230728/exp_4/families.txt 0
echo '```'
echo "### OMA.OG versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_4/families_OG.txt ../data/VectorBase/families_OG_4.txt 0
echo '```'
echo "### OMA.HOG versus PO"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_4/families_HOG.txt ./proteinortho_20230728/exp_4/families.txt 0
echo '```'
echo "### OMA.HOG versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_4/families_HOG.txt ../data/VectorBase/families_OG_4.txt 0
echo '```'
echo "### PO versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_4/families.txt ../data/VectorBase/families_OG_4.txt 0
echo '```'
echo

echo "## OMA.OG only"
echo "### 7 species, all chromosomes versus 4 species, all chromosomes"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families_OG.txt ./OMA_20230728/exp_3/families_OG.txt 1
echo '```'
echo "### 4 species, all chromosomes versus 4 species, X chromosomes"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families_OG.txt ./OMA_20230728/exp_4/families_OG.txt 1
echo '```'
echo

echo "## OMA.HOG only"
echo "### 7 species, all chromosomes versus 4 species, all chromosomes"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families_HOG.txt ./OMA_20230728/exp_3/families_HOG.txt 1
echo '```'
echo "### 4 species, all chromosomes versus 4 species, X chromosomes"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families_HOG.txt ./OMA_20230728/exp_4/families_HOG.txt 1
echo '```'
echo

echo "## PO only"
echo "### 7 species, all chromosomes versus 4 species, all chromosomes"
echo '```'
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_2/families.txt ./proteinortho_20230728/exp_3/families.txt 1
echo '```'
echo "### 4 species, all chromosomes versus 4 species, X chromosomes"
echo '```'
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_3/families.txt ./proteinortho_20230728/exp_4/families.txt 1
echo '```'




