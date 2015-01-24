from keybar.tasks import celery


class TestCeleryConfig:

    def test_simple(self):
        @celery.task
        def dummy_task():
            pass

        dummy_task.delay()

        assert True
