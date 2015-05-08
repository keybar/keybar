from keybar.utils.logging import get_logger


def test_func():
    pass


class TestClass:
    def test(self):
        pass


class TestGetLogger:
    def test_function(self):
        logger = get_logger(test_func)
        assert logger.name == 'keybar.tests.utils.test_logging.test_func'

    def test_class(self):
        logger = get_logger(TestClass)
        assert logger.name == 'keybar.tests.utils.test_logging.TestClass'

    def test_method(self):
        logger = get_logger(TestClass.test)
        assert logger.name == 'keybar.tests.utils.test_logging.TestClass.test'

    def test_string(self):
        logger = get_logger('test123')
        assert logger.name == 'test123'

    def test_fallback(self):
        logger = get_logger(None)
        assert logger.name == 'root'
