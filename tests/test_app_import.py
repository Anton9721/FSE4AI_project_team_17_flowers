def test_import_streamlit_app():
    import app.app as streamlit_app
    assert hasattr(streamlit_app, "get_infer"), "Streamlit app missing load_infer()"