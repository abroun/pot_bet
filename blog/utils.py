
def user_has_admin_rights( user ):

    email_name, domain_part = user.email.strip().rsplit( "@", 1 )

    return user.is_superuser or domain_part in [ "potatobristol.com", "potatolondon.com" ]