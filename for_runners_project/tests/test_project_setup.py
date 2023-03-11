from pathlib import Path

from bx_py_utils.test_utils.unittest_utils import assert_no_flat_tests_functions
from django.conf import settings
from django.core.cache import cache
from django.test import TestCase

import for_runners


PACKAGE_ROOT = Path(for_runners.__file__).parent.parent


class ProjectSettingsTestCase(TestCase):
    def test_project_path(self):
        project_path = settings.BASE_PATH
        assert project_path.is_dir()
        assert Path(project_path, 'for_runners').is_dir()
        assert Path(project_path, 'for_runners_project').is_dir()

    def test_template_dirs(self):
        assert len(settings.TEMPLATES) == 1
        dirs = settings.TEMPLATES[0].get('DIRS')
        assert len(dirs) == 1
        template_path = Path(dirs[0]).resolve()
        assert template_path.is_dir()

    def test_cache(self):
        # django cache should work in tests, because some tests "depends" on it
        cache_key = 'a-cache-key'
        assert cache.get(cache_key) is None
        cache.set(cache_key, 'the cache content', timeout=1)
        assert cache.get(cache_key) == 'the cache content'
        cache.delete(cache_key)
        assert cache.get(cache_key) is None

    def test_settings(self):
        self.assertEqual(settings.SETTINGS_MODULE, 'for_runners_project.settings.tests')
        middlewares = [entry.rsplit('.', 1)[-1] for entry in settings.MIDDLEWARE]
        assert 'AlwaysLoggedInAsSuperUserMiddleware' not in middlewares
        assert 'DebugToolbarMiddleware' not in middlewares

    def test_no_ignored_test_function(self):
        # In the past we used pytest ;)
        # Check if we still have some flat test function that will be not executed by unittests
        assert_no_flat_tests_functions(PACKAGE_ROOT / 'for_runners')
        assert_no_flat_tests_functions(PACKAGE_ROOT / 'for_runners_project')