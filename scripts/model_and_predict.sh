#python gather_power_data.py c17 300 30 ../data/c17_training
#python gather_power_data.py c17 300 30 ../data/c17_testing
#python gather_power_data.py c432 300 30 ../data/c432_training
#python gather_power_data.py c432 300 30 ../data/c432_testing
#python gather_power_data.py c499 300 30 ../data/c499_training
#python gather_power_data.py c499 300 30 ../data/c499_testing
#python gather_power_data.py c880 300 30 ../data/c880_training
#python gather_power_data.py c880 300 30 ../data/c880_testing
#python gather_power_data.py c1908 300 30 ../data/c1908_training
#python gather_power_data.py c1908 300 30 ../data/c1908_testing
#python gather_power_data.py c2670 300 30 ../data/c2670_training
#python gather_power_data.py c2670 300 30 ../data/c2670_testing
#python gather_power_data.py c6288 300 30 ../data/c6288_training
#python gather_power_data.py c6288 300 30 ../data/c6288_testing
#python gather_power_data.py c7552 300 30 ../data/c7552_training
#python gather_power_data.py c7552 300 30 ../data/c7552_testing

python construct_power_model.py ../data/c17_training/sequences ../data/c17_power_model
python power_model_prediction.py ../data/c17_testing/sequences ../data/c17_power_model/power_model ../data/c17_power_model/

python construct_power_model.py ../data/c432_training/sequences ../data/c432_power_model
python power_model_prediction.py ../data/c432_testing/sequences ../data/c432_power_model/power_model ../data/c432_power_model/
