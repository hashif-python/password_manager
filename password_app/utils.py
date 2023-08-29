


def validate_password(password):
    status=True
    message='Pass'
    if len(password) < 8:
        status=False
        message="Password must be at least 8 characters long."
        return {'status':status,'message':message}
    else:
        if not any(char.isupper() for char in password):
            status=False
            message="Password must contain at least one uppercase letter."
            return {'status':status,'message':message}
        else:
            if not any(char.islower() for char in password):
                status=False
                message="Password must contain at least one lowercase letter."
                return {'status':status,'message':message}
            else:
                if not any(char.isdigit() for char in password):
                    status=False
                    message="Password must contain at least one digit."
                    return {'status':status,'message':message}
                else:
                    if not any(char in '!@#$%^&*()_+[]{}|;:,.<>?/~`"\'\\' for char in password):
                        status=False
                        message="Password must contain at least one special character (!@#$%^&*()_+[]{}|;:,.<>?/~`\"'\\)."
                        return {'status':status,'message':message}
                    else:
                        return {'status':status,'message':message}

    