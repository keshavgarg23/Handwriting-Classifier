#!/bin/bash


main_folder=$1          # main_folder/classes type format
test_ratio=15          #percentage
validate_ratio=0          



names=$(ls $main_folder)
train='dataset_model/train'
test='dataset_model/test'
validate='dataset_model/validate'

mkdir dataset_model
mkdir $train
mkdir $test
mkdir $validate

for name in $names
do
    total=`ls -l $main_folder/$name | wc -l`        # finding total files
    test_count=`expr $total \* $test_ratio`         # exact number of test_files
    validate_count=`expr $total \* $validate_ratio`
    test_count=`expr $test_count \/ 100`            # since calculated as percentage converting to actual countcle
    validate_count=`expr $validate_count \/ 100`

    echo -e $main_folder/$name  $total $test_count $validate_count


    # test
    move_files_test=$(ls $main_folder/$name | shuf -n $test_count)
    mkdir $test/$name
    for file in $move_files_test
    do
        mv $main_folder/$name/$file $test/$name
    done


    # validate
    move_files_vali=$(ls $main_folder/$name | shuf -n $validate_count)
    mkdir $validate/$name
    for file in $move_files_vali
    do
        mv $main_folder/$name/$file $validate/$name
    done

    # train
    mkdir $train/$name
    for file in `ls $main_folder/$name`
    do 
        mv $main_folder/$name/$file $train/$name
    done

done