
# Overview

This **Python 3.X** repository contains algorithms to enable the approximation of the **Virtual Network Embedding Algorithm (VNEP)**. 
It makes extensive use of our **[alib](https://github.com/vnep-approx-py3/alib)** library. In particular, our algorithms employ
Gurobi to compute convex combinations of valid mappings to apply **randomized rounding**. We provide the following implementations: 

- A Linear Program (LP) implementation based on our papers [1,2] for cactus request graphs 
**[modelcreator_ecg_decomposition.py](vnep_approx/modelcreator_ecg_decomposition.py)**.
- A Linear Program based on our generalized extraction width concept for arbitrary requests based on our paper [3]: 
**[commutativity_model.py](vnep_approx/commutativity_model.py)**
- A Linear Program enabling the handling of decisions (outgoing edges represent choices) extending the formulation presented in [4]: **[gadget_model.py](vnep_approx/gadget_model.py)**.
- A implementation of randomized rounding for cactus request graphs **[randomized_rounding_triumvirate.py](vnep_approx/randomized_rounding_triumvirate.py)**. 
This randomized rounding procedure actually executed three different kinds of heuristics:
  - **Vanilla rounding**: simply round solutions and select the best one found within a fixed number of iterations (see [2,6]).
  - **Heuristic rounding**: perform the rounding while discarding selected (i.e. rounded) mappings whose addition would 
  exceed resource capacities. Accordingly: this heuristic always yields feasible solutions (see [2,6]).
  - **Multi-dimensional knapsack (MDK)**: given the decomposition into convex combinations of valid mappings for each request,
  the MDK computes the optimal rounding given all mapping possibilities found.
- An implementation of randomized rounding based on a column generation / separation LP approach presented in [5]: using the DynVMP algorithm valid mappings are priced into the LP, where the runtime of DynVMP is polynomial in the input size and exponential in the **tree width** of the request graphs. All code pertaining to this approach can be found in the **[treewidth_model.py](vnep_approx/treewidth_model.py)**.
- An implementation of the ViNE online heuristics and their offline counterpart WiNE: **[vine.py](vnep_approx/vine.py)** 
  

Note that our separate Github repositories [evaluation-ifip-networking-2018](https://github.com/vnep-approx/evaluation-ifip-networking-2018) and [evaluation-acm-ccr-2019](https://github.com/vnep-approx/evaluation-acm-ccr-2019)
provide more explanatiosn on how to generate scenarios and apply algorithms. 

## Papers

**[1]** Matthias Rost, Stefan Schmid: Service Chain and Virtual Network Embeddings: Approximations using Randomized Rounding. [CoRR abs/1604.02180](https://arxiv.org/abs/1604.02180) (2016)

**[2]** Matthias Rost, Stefan Schmid: Virtual Network Embedding Approximations: Leveraging Randomized Rounding. IFIP Networking 2018. (see [arXiv](https://arxiv.org/abs/1803.03622) for the corresponding technical report)

**[3]** Matthias Rost, Stefan Schmid: (FPT-)Approximation Algorithms for the Virtual Network Embedding Problem. [CoRR abs/1803.04452](https://arxiv.org/abs/1803.04452) (2018)

**[4]** Guy Even, Matthias Rost, Stefan Schmid: An Approximation Algorithm for Path Computation and Function Placement in SDNs. [SIROCCO 2016: 374-390](https://link.springer.com/chapter/10.1007%2F978-3-319-48314-6_24)

**[5]** Matthias Rost, Elias Döhne, Stefan Schmid: Parametrized Complexity of Virtual Network Embeddings: Dynamic & Linear Programming Approximations. [ACM CCR January 2019](https://ccronline.sigcomm.org/wp-content/uploads/2019/02/sigcomm-ccr-final255.pdf)

**[6]** Matthias Rost, Stefan Schmid: Virtual network embedding approximations: Leveraging randomized rounding. [IEEE/ACM Transactions on Networking 27 (5), 2019.](https://ieeexplore.ieee.org/abstract/document/8846601)


# Dependencies and Requirements

The **vnep_approx** library requires Python 3.X. Required python libraries are gurobipy, numpy, matplotlib, click, and  **[alib](https://github.com/vnep-approx-py3/alib)**.

Furthermore, we use Tamaki's algorithm presented in his [paper at ESA 2017](http://drops.dagstuhl.de/opus/volltexte/2017/7880/pdf/LIPIcs-ESA-2017-68.pdf) to compute tree decompositions (efficiently). The corresponding GitHub repository [TCS-Meiji/PACE2017-TrackA](https://github.com/TCS-Meiji/PACE2017-TrackA) must be cloned locally and the environment variable **PACE_TD_ALGORITHM_PATH** must be set to point the location of the repository: PACE_TD_ALGORITHM_PATH="$PATH_TO_PACE/PACE2017-TrackA".
Gurobi must be installed and the .../gurobi64/lib directory added to the environment variable LD_LIBRARY_PATH.

For generating and executing (etc.) experiments, the environment variable **ALIB_EXPERIMENT_HOME** should be set to a path,
such that the subfolders input/ output/ and log/ exist. If this environment variable is not set, the current working directory is traversed upwards until a directory containing input/, output/, and log/ is found.

**Note**: Our source was tested on Linux (specifically Ubuntu 14 and Ubuntu 16) and Mac OS X 10.15.  

# Overview

To install **vnep_approx**, we provide a setup script. Simply execute from within vnep_approx's root directory: 

```
pip install .
```

Furthermore, if the code base will be edited by you, we propose to install it as editable:
```
pip install -e .
```
When choosing this option, sources are not copied during the installation but the local sources are used: changes to
the sources are directly reflected in the installed package.

We generally propose to install **vnep_approx** into a virtual environment (together with **alib**).

# Usage

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

# Tests


The test directory contains a large number of tests to check the correctness of our implementation and might also be useful
to understand the code. 

To execute the tests, simply execute pytest in the test directory.

```
pytest .
```

Some tests use extensive logging in case of failures. In the [conftest.py](test/conftest.py), we overwrite some default logging behaviours 
to better suit our needs. In particular, you may use the following options:

```
--log-cli-level     determines whether and if log outputs are output via stdout (the cli)
--log-level         determines the log level of messages to be written in a log file
--log-file          determines the name of the log file to be written; if not given no log file is written
```

Importantly, log files are always created within separate directories. The (fixed) naming scheme is as follows:
```
log_YYYY_MM_DD_HH_X
```
where X denotes a counter that is automatically incremented.

## pytest-xdist

Our changes to the logging behaviour facilitate the usage of pytest-xdist to parallelize test execution. If pytest-xdist is installed and used, then
for each worker a separate log file is created and written to. The name of the log files is derived from the file base of the --log-level option.
For example, using the following command
```
pytest -n 4 --log-file log.log --log-level debug .
```
the following log files are created:
```
log_YYYY_MM_DD_HH_X
|_ log_worker_0.log
|_ log_worker_1.log
|_ log_worker_2.log
|_ log_worker_3.log
```

# API Documentation

We provide a basic template to create an API documentation using **[Sphinx](http://www.sphinx-doc.org)**. 

To create the documentation, simply execute the makefile in **[docs/](docs/)**. Specifically, run for example

```
make html
```
to create the HTML documentation.

Note that **alib** must lie on the PYTHONPATH. If you use a virtual environment, we propose to install sphinx within the
virtual environment (using **pip install spinx**) and executing the above from within the virtual environment. 

# Contact and Acknowledgement

If you have any questions, either open up an issue on GitHub or write a mail to robin.muenk@tum.de
