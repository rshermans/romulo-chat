import os
import sys
import importlib
import pandas as pd

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_convert_df_returns_bytes_with_header():
    module = importlib.import_module('streamlit_app')
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    result = module.convert_df(df)

    assert isinstance(result, bytes)
    assert result.startswith(b'col1,col2')
