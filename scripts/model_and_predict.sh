for module in c17; do
    for model in 4d_table linear quadratic cubic; do
        python construct_power_model.py ../data/${module}_training/sequences ${model} ../models/${module}_power_model ${model}_power_model
    done
done
