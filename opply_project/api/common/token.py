import uuid

# Check if a string is a valid UUID
def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test

# Get the public user id from the token in the request
def get_user_public_id_from_token(request):
    # Get all token claims
    token = request.auth
    claims = token.payload

    if not claims:
        return None
    
    public_id = claims.get('public_id')

    print('public_id', public_id)

    if not public_id or not is_valid_uuid(public_id):
        return None
    
    return public_id
