# Password Instructions for Judging Service

## New Password Format

All user passwords now follow a consistent format:

```
username_password
```

## Examples

- For user with username `tkachenko_i`, the password is `tkachenko_i_password`
- For user with username `yosypenko_o`, the password is `yosypenko_o_password`
- For user with username `chernikov_s`, the password is `chernikov_s_password`

## For Judges

If you're having trouble logging in, please use the format described above. If you still can't log in, please contact the administrator.

## For Administrators

If users are having trouble logging in, you can run the following command to update all passwords to the new format:

```bash
python manage.py update_passwords
```

This will update all non-superuser users' passwords to follow the consistent format.