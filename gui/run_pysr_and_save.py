import os
import pandas as pd
import traceback as tb
import numpy as np
from pysr import PySRRegressor
from argparse import ArgumentParser

# Args:
# niterations
# binary_operators
# unary_operators
# col_to_fit

empty_df = pd.DataFrame(
    {
        "equation": [],
        "loss": [],
        "complexity": [],
    }
)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--niterations", type=int)
    parser.add_argument("--maxsize", type=int)
    parser.add_argument("--binary_operators", type=str)
    parser.add_argument("--unary_operators", type=str)
    parser.add_argument("--col_to_fit", type=str)
    parser.add_argument("--filename", type=str)
    args = parser.parse_args()
    niterations = args.niterations
    binary_operators = eval(args.binary_operators)
    unary_operators = eval(args.unary_operators)
    col_to_fit = args.col_to_fit
    filename = args.filename
    maxsize = args.maxsize


    df = pd.read_csv(filename)
    y = np.array(df[col_to_fit])
    X = df.drop([col_to_fit], axis=1)

    model = PySRRegressor(
        progress=False,
        verbosity=0,
        maxsize=maxsize,
        niterations=niterations,
        binary_operators=binary_operators,
        unary_operators=unary_operators,
    )
    model.fit(X, y)

    df = model.equations_[["equation", "loss", "complexity"]]
    # Convert all columns to string type:
    df = df.astype(str)
    error_message = (
            "Success!\n"
            f"You may run the model locally (faster) with "
            f"the following parameters:"
            +f"""
model = PySRRegressor(
    niterations={niterations},
    binary_operators={str(binary_operators)},
    unary_operators={str(unary_operators)},
    maxsize={maxsize},
)
model.fit(X, y)""")

    df.to_csv("pysr_output.csv", index=False)
    with open("error.log", "w") as f:
        f.write(error_message)
