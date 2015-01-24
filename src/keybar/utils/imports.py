import pkgutil


_imported = set()


def import_submodules(context, root_module, path):
    """
    Import all submodules and register them in the ``context`` namespace.

    ``import_submodules(globals(), __name__, __path__)``
    """
    for loader, module_name, is_pkg in pkgutil.walk_packages(path):
        if ((module_name, tuple(path))) in _imported:
            continue

        module = loader.find_module(module_name).load_module(module_name)
        for k, v in vars(module).items():
            if not k.startswith('_'):
                context[k] = v
        context[module_name] = module
        _imported.add((module_name, tuple(path)))
