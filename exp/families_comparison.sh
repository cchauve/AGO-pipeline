echo "## 7 species, all chromosomes"
echo "### OMA versus PO"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families.txt ./proteinortho_20230728/exp_2/families.txt 0
echo '```'
echo "### OMA versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families.txt ../data/VectorBase/families_OG_2.txt 0
echo '```'
echo "### PO versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_2/families.txt ../data/VectorBase/families_OG_2.txt 0
echo '```'
echo

echo "## 4 species, all chromosomes"
echo "### OMA versus PO"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families.txt ./proteinortho_20230728/exp_3/families.txt 0
echo '```'
echo "### OMA versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families.txt ../data/VectorBase/families_OG_3.txt 0
echo '```'
echo "### PO versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_3/families.txt ../data/VectorBase/families_OG_3.txt 0
echo '```'
echo

echo "## 4 species, X chromosome"
echo "### OMA versus PO"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_4/families.txt ./proteinortho_20230728/exp_4/families.txt 0
echo '```'
echo "### OMA versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_4/families.txt ../data/VectorBase/families_OG_4.txt 0
echo '```'
echo "### PO versus VectoBase.OG"
echo '```'
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_4/families.txt ../data/VectorBase/families_OG_4.txt 0
echo '```'
echo

echo "## OMA only"
echo "### 7 species, all chromosomes versus 4 species, all chromosomes"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families.txt ./OMA_20230728/exp_3/families.txt 1
echo '```'
echo "### 4 species, all chromosomes versus 4 species, X chromosomes"
echo '```'
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families.txt ./OMA_20230728/exp_4/families.txt 1
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




