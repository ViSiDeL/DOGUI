import re
from api.models.inference import generate_text

def _clean_generated_code(raw_code: str) -> str:
    unwanted_patterns = [
        r'var\s+scene\s*=\s*new\s+THREE\.Scene\(\);?',
        r'var\s+camera\s*=\s*new\s+THREE\.PerspectiveCamera\([^;]*\);?',
        r'var\s+renderer\s*=\s*new\s+THREE\.WebGLRenderer\([^;]*\);?',
        r'renderer\.setSize\([^;]*\);?',
        r'document\.body\.appendChild\([^;]*\);?',
        r'renderer\.render\([^;]*\);?',
    ]
    for pattern in unwanted_patterns:
        raw_code = re.sub(pattern, '', raw_code, flags=re.IGNORECASE)
    for marker in ['```javascript', '```', '[RESP]', '// THREE.JS CODE START', '// THREE.JS CODE END']:
        raw_code = raw_code.replace(marker, '')
    cleaned = '\n'.join(
        line.strip() for line in raw_code.split('\n')
        if line.strip() and not line.strip().startswith(('//', '/*', '*', '*/'))
    ).strip()
    if not cleaned.endswith(';'):
        cleaned += ';'
    return cleaned

def generate_threejs_snippet(user_description: str) -> str:

    prompt = f"""
You are a three.js generator.
Here is their description: "{user_description}".

Generate a concise, syntactically correct three.js snippet that fulfills the description.
Provide only the JavaScript code without extra explanations or markdown fences.
Respond with raw JavaScript statements (e.g., creating a scene, camera, renderer, etc.).
"""
    response_text = generate_text(prompt=prompt, max_tokens=900)
    return _clean_generated_code(response_text)