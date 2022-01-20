
# Overview

This **Python 3** repository contains an extension of approximation algorithms for the **Virtual Network Embedding Algorithm (VNEP)**, adapting them to also account for **Latency Constraints**. The implementation is largely based on the original framework at **[github.com/vnep-approx-py3](https://github.com/vnep-approx-py3)** while the theoretical results are thoroughly laid out in our Technical Report **[1]** and our shortened paper **[2]**, as published in IFIP Networking 2021 Poster Session. The repository contains the implementation of our novel algorithm **FLEX**.

For a more thorough overview of the algorithms, its usages, docs and test, simply view the [Original Implementation](https://github.com/vnep-approx-py3) and consult the corresponding papers.

### Structure

This GitHub Organization contains three repositories which contain the functionality for solving the VNEP with latency constraints and evaluating the results: 

- **[alib](https://github.com/vnep-approx-latency/alib)**: A library providing the basic data model and the Mixed-Integer Program for the classic multi-commodity formulation.
- **[vnep_approx](https://github.com/vnep-approx-latency/vnep-approx)**: Provides Linear Programming formulations, specifically the one based on the DynVMP algorithm, as well as Randomized Rounding algorithms to solve the VNEP.
- **[evaluation-ifip-networking-2021](https://github.com/vnep-approx-latency/evaluation-ifip-networking-2021)**: Provides functionality for evaluating experiment artifacts to create plots to compare runtime, profits and other algorithm parameters.

### Papers

**[1]** R. Münk, M. Rost, S. Schmid, and H. Räcke. It’s Good to Relax: Fast Profit Approximation for Virtual Networks with Latency Constraints. [Technical Report arXiv:2104.09249 [cs.NI]](https://arxiv.org/abs/2104.09249), April 2021.

**[2]** R. Münk, M. Rost, H. Räcke and S. Schmid, It's Good to Relax: Fast Profit Approximation for Virtual Networks with Latency Constraints, *2021 IFIP Networking Conference (IFIP Networking)*, 2021, pp. 1-3, doi: [10.23919/IFIPNetworking52078.2021.9472197](https://ieeexplore.ieee.org/document/9472197).


# Dependencies and Requirements

The **vnep_approx** library requires Python 3.7 and heavily relies on the **[alib](https://github.com/vnep-approx-latency/alib)** package..

The [Gurobi Solver](https://www.gurobi.com/) must be installed and the .../gurobi64/lib directory added to the environment variable LD_LIBRARY_PATH.

Furthermore, we use Tamaki's algorithm presented in his [paper at ESA 2017](http://drops.dagstuhl.de/opus/volltexte/2017/7880/pdf/LIPIcs-ESA-2017-68.pdf) to compute tree decompositions (efficiently). The corresponding GitHub repository [TCS-Meiji/PACE2017-TrackA](https://github.com/TCS-Meiji/PACE2017-TrackA) must be cloned locally and the environment variable **PACE_TD_ALGORITHM_PATH** must be set to point the location of the repository: PACE_TD_ALGORITHM_PATH="$PATH_TO_PACE/PACE2017-TrackA".

# Installation

Install each of the **[alib](https://github.com/vnep-approx/alib)** and **vnep_approx** packages using the setup script we provide. Simply execute from within each of the packages root directories: 

```
pip install -e .
```

When choosing the `-e` option, sources are not copied during the installation but the local sources are used: changes to the sources are directly reflected in the installed package.

We generally recommend installing our libraries in a virtual environment.

# Usage

**For a detailed walk-through of how to use the algorithms and reproduce the results from the paper, please view the examples in the** [**evaluation-ifip-networking-2021**](https://github.com/vnep-approx-latency/evaluation-ifip-networking-2021) **repository.**

For generating and executing (etc.) experiments, the environment variable **ALIB_EXPERIMENT_HOME** should be set to a path, such that the subfolders input/ output/ and log/ exist. If this environment variable is not set, the current working directory is traversed upwards until a directory containing input/, output/, and log/ is found.

You may either use our code via our API by importing the library or via our command line interface:

```
python -m vnep_approx.cli                                                                                     
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate-scenarios  generates scenarios according to a yaml file; simply
                      calls the functionality of the alib

  start-experiment    starts an experiment specified in a yaml file; uses
                      essentially the functionality of the alib but loads
                      several algorithm contained in this library
```

Both generating scenarios and running an experiment requires a different YAML file which contains the necessary configuration. Examples can be found in the examples folder.

## Example 

An example execution using the **alib** and **vnep-approx** packages can the be started like follows. This assumes that the **ALIB_EXPERIMENT_HOME** environment variable is set as described above and also the **LATENCY_FILES_HOME**  environment variable points to a folder that contains the configuration files `example_scenarios.yml` and `example_execution.yml`. Suggestions for these configuration files are provided in the /examples folder. 

First run the following command to generate the scenarios.

````
python -m vnep_approx.cli generate-scenarios scenarios.pickle $LATENCY_FILES_HOME/example_scenarios.yml
````

This will create the file `scenarios.pickle` in the /output folder of the **ALIB_EXPERIMENT_HOME** directory. Move it to the /input folder and execute the following.

````
python -m vnep_approx.cli start-experiment $LATENCY_FILES_HOME/example_execution.yml 0 10000 --concurrent 8 --overwrite_existing_intermediate_solutions --remove_intermediate_solutions
````

The result will be the file `example_results.pickle`. To evaluate these results, use the functionality provided in the  [evaluation-ifip-networking-2021](https://github.com/vnep-approx-latency/evaluation-ifip-networking-2021) repository.

# Contact

If you have any questions, either open up an issue on GitHub or write a mail to [robin.muenk@tum.de](mailto:robin.muenk@tum.de).
