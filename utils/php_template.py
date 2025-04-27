import os
from typing import Dict

class PHPTemplateHandler:
    def __init__(self, template_dir: str = 'payloads'):
        self.template_dir = template_dir
        
    def render_template(self, template_name: str, variables: Dict[str, str]) -> str:
        """
        Render a PHP template with variables
        
        Args:
            template_name: Name of template file
            variables: Dictionary of variables to replace in template
            
        Returns:
            Rendered template content
        """
        template_path = os.path.join(self.template_dir, template_name)
        
        with open(template_path, 'r') as f:
            content = f.read()
            
        for key, value in variables.items():
            content = content.replace(f"{{{key}}}", value)
            
        return content