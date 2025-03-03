from fsrs_rs_python import DEFAULT_PARAMETERS, default_simulator_config, simulate

if __name__ == "__main__":
    config = default_simulator_config()
    config.learn_span = 10

    print(simulate(DEFAULT_PARAMETERS, 0.9, config).cost_per_day)
    print(simulate(DEFAULT_PARAMETERS, 0.9, default_simulator_config()).cost_per_day)
