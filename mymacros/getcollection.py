from mkdocs_macros.plugin import MacrosPlugin

def define_env(env):
    @env.macro
    def getcollection_items(collection_name, limit=5):
        """Generates HTML list items for a collection"""
        nav = env.conf['nav']
        collection = next((item for item in nav if isinstance(item, dict) and collection_name in item), None)
        
        if not collection:
            return f"<!-- Collection '{collection_name}' not found -->"
            
        items = collection[collection_name]
        html = []
        for item in items[:limit]:
            if isinstance(item, dict):
                title = next(iter(item.keys()))
                path = item[title]
                html.append(f'<li><a href="{path}">{title}</a></li>')
            elif isinstance(item, str):
                html.append(f'<li><a href="{item}">{item.split("/")[-1].replace(".md", "")}</a></li>')
        
        return f'<ul class="collection-list">{"".join(html)}</ul>'