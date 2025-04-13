from .plugin import AIResourcesPlugin

# This makes the plugin visible to MkDocs
def get_plugin():
    return AIResourcesPlugin()