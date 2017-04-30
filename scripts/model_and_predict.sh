for module in c17 c1908 c2670 c432 c499 c6288 c7552 c880; do
    for model in 4d_table linear quadratic cubic; do
        python construct_power_model.py ../data/${module}_training/sequences ${model} ../models/${module}_power_model ${model}_power_model
        python power_model_prediction.py ../data/${module}_testing/sequences ../models/${module}_power_model/${model}_power_model ${model} ../models/${module}_power_model/${model}_error
    done
done
