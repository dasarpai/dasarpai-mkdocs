# mymacros/__init__.py

__version__ = "1.0.0"
__all__ = ['audioemb', 'getcollection']  # Explicit module exports

# Optional initialization hook (not required for mkdocs-macros)
def __initialize_macros__():
    """Called automatically when mkdocs-macros loads this package"""
    from . import audioemb, getcollection
    return [audioemb, getcollection]