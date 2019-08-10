import handout

def test_get_logger_has_single_handler(): 
    import handout # Simulate multiple imports of a package.
    import handout
    logger = handout.logger.get_logger()
    assert len(logger.handlers) == 1 