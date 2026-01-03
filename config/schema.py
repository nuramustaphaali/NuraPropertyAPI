# config/schema.py
def djoser_tag_fix(result, generator, request, public):
    """
    This function intercepts the schema generation.
    It looks for any endpoint starting with '/api/v1/auth/' 
    and forces the tag to be 'Authentication'.
    """
    paths = result.get('paths', {})
    
    for path, methods in paths.items():
        # Check if the URL belongs to Djoser/Auth
        if path.startswith('/api/v1/auth/'):
            for method, config in methods.items():
                # Force the tag to be "Authentication"
                config['tags'] = ['Authentication']
                
    return result