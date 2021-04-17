import gurobipy
import pytest

import gurobi_mock
import os
import glob
import logging
import datetime
from time import sleep

import alib.util as util


@pytest.fixture
def mock_gurobi(monkeypatch):
    monkeypatch.setattr(gurobipy, "LinExpr", gurobi_mock.MockLinExpr)
    monkeypatch.setattr(gurobipy, "Model", gurobi_mock.MockModel)


@pytest.fixture
def import_gurobi_mock():
    return gurobi_mock


def pytest_configure(config):
    log_file = config.getoption('log_file')
    if log_file is None:
        log_file = config.getini('log_file')

    log_level_opt = config.getoption('log_level')
    if log_level_opt is None:
        log_level_opt = config.getini('log_level')
    if log_level_opt:
        log_level_file = getattr(logging, log_level_opt.upper(), None)
        if not log_level_file:
            raise RuntimeError('Invalid log-level option: {}'.format(log_level_opt))
    else:
        log_level_file = logging.DEBUG

    log_level_cli_opt = config.getoption("log_cli_level")
    if log_level_cli_opt is None:
        log_level_cli_opt = config.getini("log_cli_level")
    if log_level_cli_opt:
        log_level_cli = getattr(logging, log_level_cli_opt.upper(), None)
        if not log_level_cli:
            raise RuntimeError(f"Invalid log-level option: {log_level_cli_opt}")
    else:
        log_level_cli = None

    if log_file:
        if 'PYTEST_XDIST_WORKER' in os.environ:
            #parallelization is enabled --> create folder
            worker_string = os.environ.get('PYTEST_XDIST_WORKER', '-1')
            numeric_worker_string = int("".join([a for a in worker_string if a.isdigit()]))
            if numeric_worker_string > -1:
                sleep(1)        #to force the main process to create the directory

            actual_log_file = log_file[0:-4] + f"_worker_{numeric_worker_string}" + ".log"

            counter = 0
            directory = "log_{}".format(datetime.datetime.now().strftime("%Y_%m_%d_%H"))
            actual_directory = directory + "_{:04d}".format(counter)

            # search for a directory name where the respective log file was not yet created
            while os.path.exists(actual_directory) and os.path.exists(os.path.join(actual_directory, actual_log_file)):
                counter += 1
                actual_directory = directory + "_{:04d}".format(counter)
            if not os.path.exists(actual_directory):
                #this should hopefully only be created by the main process
                os.mkdir(actual_directory)

            actual_log_file = os.path.join(actual_directory,actual_log_file)

            util.initialize_root_logger(actual_log_file, print_level=log_level_cli, file_level=log_level_file,
                                        allow_override=True)

            logging.getLogger().info(f"Setting up logging in file {actual_log_file} ({log_level_file}) and via cli ({log_level_cli is not None}) ({log_level_cli})")

        else:
            counter = 0
            directory = "log_{}".format(datetime.datetime.now().strftime("%Y_%m_%d_%H"))
            actual_directory = directory + "_{:04d}".format(counter)

            # search for a directory that does not yet exist
            while os.path.exists(actual_directory):
                counter += 1
                actual_directory = directory + "_{:04d}".format(counter)
            os.mkdir(actual_directory)

            actual_log_file = os.path.join(actual_directory, log_file)

            util.initialize_root_logger(actual_log_file, print_level=log_level_cli, file_level=log_level_file,
                                        allow_override=True)
            logging.getLogger().info(f"Setting up logging in file {actual_log_file} ({log_level_file}) and via cli ({log_level_cli is not None}) ({log_level_cli})")
    else:
        if log_file:
            actual_log_file = os.path.join("./", log_file)
        else:
            actual_log_file = None

        util.initialize_root_logger(actual_log_file, print_level=log_level_cli, file_level=log_level_file,
                                    allow_override=True)
        logging.getLogger().info(
            f"Setting up logging in file {actual_log_file} ({log_level_file}) and via cli ({log_level_cli is not None}) ({log_level_cli})")