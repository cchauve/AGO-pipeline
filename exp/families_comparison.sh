echo "# 7 species, all chromosomes"
echo "## OMA versus proteinortho"
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families.txt ./proteinortho_20230728/exp_2/families.txt 0
echo "## OMA versus VectoBase.OG"
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families.txt ../data/VectorBase/families_OG_2.txt 0
echo "## proteinortho versus VectoBase.OG"
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_2/families.txt ../data/VectorBase/families_OG_2.txt 0
echo

echo "# 4 species, all chromosomes"
echo "## OMA versus proteinortho"
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families.txt ./proteinortho_20230728/exp_3/families.txt 0
echo "## OMA versus VectoBase.OG"
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families.txt ../data/VectorBase/families_OG_3.txt 0
echo "## proteinortho versus VectoBase.OG"
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_3/families.txt ../data/VectorBase/families_OG_3.txt 0
echo

echo "# 4 species, X chromosome"
echo "## OMA versus proteinortho"
python ../scripts/family_utils.py compare ./OMA_20230728/exp_4/families.txt ./proteinortho_20230728/exp_4/families.txt 0
echo "## OMA versus VectoBase.OG"
python ../scripts/family_utils.py compare ./OMA_20230728/exp_4/families.txt ../data/VectorBase/families_OG_4.txt 0
echo "## proteinortho versus VectoBase.OG"
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_4/families.txt ../data/VectorBase/families_OG_4.txt 0
echo

echo "# OMA only"
echo "## 7 species, all chromosomes versus 4 species, all chromosomes"
python ../scripts/family_utils.py compare ./OMA_20230728/exp_2/families.txt ./OMA_20230728/exp_3/families.txt 1
echo "## 4 species, all chromosomes versus 4 species, X chromosomes"
python ../scripts/family_utils.py compare ./OMA_20230728/exp_3/families.txt ./OMA_20230728/exp_4/families.txt 1
echo

echo "# proteinortho only"
echo "## 7 species, all chromosomes versus 4 species, all chromosomes"
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_2/families.txt ./proteinortho_20230728/exp_3/families.txt 1
echo "## 4 species, all chromosomes versus 4 species, X chromosomes"
python ../scripts/family_utils.py compare ./proteinortho_20230728/exp_3/families.txt ./proteinortho_20230728/exp_4/families.txt 1
echo



