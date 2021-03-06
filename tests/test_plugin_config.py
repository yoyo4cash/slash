import pytest
import slash
from slash.plugins import PluginInterface


@pytest.fixture(autouse=True)
def restore_plugins(request):
    request.addfinalizer(slash.plugins.manager.install_builtin_plugins)
    request.addfinalizer(slash.plugins.manager.uninstall_all)


def test_plugin_config():

    assert 'sample' not in slash.config['plugin_config']
    value = object()

    class Plugin(PluginInterface):

        def get_name(self):
            return 'sample'

        def get_config(self):
            return {
                'values': {
                    'value_1': value,
                }}

    slash.plugins.manager.install(Plugin())

    assert slash.config.root.plugin_config.sample.values.value_1 is value

    slash.plugins.manager.uninstall('sample')

    assert 'sample' not in slash.config['plugin_config']
