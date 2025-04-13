import re
import os
from mkdocs.plugins import BasePlugin

class AIResourcesPlugin(BasePlugin):
    config_scheme = (
        ('resources_file', str, 'docs/assets/docs/all-ai-resources.md'),
    )
    
    def on_config(self, config):
        """
        Handle configuration setup
        """
        self.resources_file = self.config.get('resources_file', 'docs/assets/docs/all-ai-resources.md')
        # Make path relative to docs_dir
        if not os.path.isabs(self.resources_file):
            # Check if it's already relative to docs_dir or absolute
            if not os.path.exists(os.path.join(config['docs_dir'], self.resources_file)):
                self.resources_file = os.path.join(config['docs_dir'], self.resources_file)
        return config
    
    def on_page_markdown(self, markdown, page, config, files):
        """
        Replace {{AI_RESOURCES}} marker with processed content
        """
        if '{{AI_RESOURCES}}' in markdown:
            resources_content = self._get_resources_content()
            processed_content = self._process_resources_content(resources_content)
            markdown = markdown.replace('{{AI_RESOURCES}}', processed_content)
        
        return markdown
    
    def _get_resources_content(self):
        """
        Read the external resources file
        """
        try:
            with open(self.resources_file, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Warning: Resources file not found at {self.resources_file}")
            return "## No Resources Available"
    
    def _process_resources_content(self, content):
        """
        Process the resources content and convert to HTML
        """
        # Split by second-level headings
        sections = re.split(r'## ', content)
        
        html_output = '<div class="ai-resources-container">\n'
        
        for section in sections:
            if not section.strip():
                continue
                
            # Extract category name and content
            lines = section.split('\n', 1)
            category_name = lines[0].strip()
            
            if category_name and category_name != "No Resources Available":
                section_content = lines[1] if len(lines) > 1 else ""
                
                # Check if there's a paragraph after the heading (separated by ".:.") 
                para_text = ""
                content_after = section_content
                
                if ".:." in section_content:
                    parts = section_content.split(".:.", 1)
                    para_text = parts[0].strip()
                    content_after = parts[1].strip()
                
                # Start building the details element
                html_output += f'<details class="category">\n'
                html_output += f'  <summary>\n'
                html_output += f'    <h2 id="{self._slugify(category_name)}">{category_name}</h2>\n'
                html_output += f'  </summary>\n\n'
                
                # Add paragraph if it exists
                if para_text:
                    html_output += f'  <p>{para_text}</p>\n\n'
                
                # Process list items
                html_output += '  <div class="content">\n'
                html_output += '    <ol>\n'
                
                # Split by numbered list items
                items = re.split(r'\s*\d+\.\s+', content_after)
                for item in items:
                    item = item.strip()
                    if not item:
                        continue
                    
                    # Handle different item formats
                    html_output += '      <li>\n'
                    
                    # Check if there's extra text after a link (separated by "::")
                    extra_text = ""
                    if "::" in item:
                        main_part, extra_text = item.split("::", 1)
                        item = main_part.strip()
                        extra_text = extra_text.strip()
                    
                    # Process Markdown links
                    link_match = re.search(r'\[(.*?)\]\((.*?)\)', item)
                    if link_match:
                        link_text = link_match.group(1)
                        link_url = link_match.group(2)
                        html_output += f'        <a href="{link_url}" target="_blank">{link_text}</a>\n'
                        
                        if extra_text:
                            html_output += f' {extra_text}\n'
                    elif "http" in item:
                        # Handle plain URLs
                        html_output += f'        <a href="{item}" target="_blank">{item}</a>\n'
                        
                        if extra_text:
                            html_output += f' {extra_text}\n'
                    else:
                        # Handle plain text
                        html_output += f'        {item}\n'
                        
                        if extra_text:
                            html_output += f' {extra_text}\n'
                    
                    html_output += '      </li>\n'
                
                html_output += '    </ol>\n'
                html_output += '  </div>\n'
                html_output += '</details>\n'
        
        html_output += '</div>'
        return html_output
    
    def _slugify(self, text):
        """
        Simple slugify function
        """
        return text.lower().replace(' ', '-')