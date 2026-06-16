def test_imports_package_and_exposes_chart():
    import imfcharts

    assert hasattr(imfcharts, "Chart")
    assert callable(imfcharts.read)
