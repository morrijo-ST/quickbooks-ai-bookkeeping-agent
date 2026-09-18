from pathlib import Path
import numpy as np
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]/'app.py'
def app():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception
    return at

def test_duplicate_review_and_session_decision():
    at=app()
    at.slider[0].set_value(.60).run()
    all_rows=at.dataframe[-1].value
    duplicates=all_rows.duplicated(['merchant','date','amount'],keep=False)
    assert duplicates.sum()==6
    assert all_rows.loc[duplicates,'decision'].eq('Review').all()
    at.button[0].click().run()
    assert not at.exception
    assert len(at.session_state['decisions'])==1
