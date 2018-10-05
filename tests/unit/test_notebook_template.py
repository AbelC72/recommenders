import os
import pytest
import pandas as pd
import papermill as pm


OUTPUT_NOTEBOOK = "output.ipynb"


@pytest.fixture(scope="module")
def notebooks():
    folder_notebooks = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), os.path.pardir, os.path.pardir, "notebooks"
        )
    )
    paths = {"template": os.path.join(folder_notebooks, "template.ipynb")}
    return paths


@pytest.mark.notebooks
def test_template_notebook_runs(notebooks):
    notebook_path = notebooks["template"]
    pm.execute_notebook(
        notebook_path, OUTPUT_NOTEBOOK, parameters=dict(pm_version=pm.__version__)
    )
    nb = pm.read_notebook(OUTPUT_NOTEBOOK)
    df = nb.dataframe
    assert df.shape[0] == 2
    check_version = df.loc[df["name"] == "checked_version", "value"].values[0]
    assert check_version is True


@pytest.mark.notebooks
def test_teamplate_notebook_fails(notebooks):
    notebook_path = notebooks["template"]
    with pytest.raises(Exception):
        pm.execute_notebook(
            notebook_path, OUTPUT_NOTEBOOK, parameters=dict(pm_version="0.1")
        )

