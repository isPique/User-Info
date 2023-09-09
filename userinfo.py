import subprocess
import win32net
import ctypes
from ctypes import wintypes
from time import sleep
from os import system

advapi32 = ctypes.WinDLL('advapi32')
netapi32 = ctypes.WinDLL('netapi32')
kernel32 = ctypes.WinDLL('kernel32')

MAX_PREFERRED_LENGTH = -1
NERR_Success = 0
ERROR_ACCESS_DENIED = 5

class USER_INFO_3(ctypes.Structure):
    _fields_ = [
        ("usri3_name", wintypes.LPWSTR),
        ("usri3_password", wintypes.LPWSTR),
        ("usri3_password_age", wintypes.DWORD),
        ("usri3_priv", wintypes.DWORD),
        ("usri3_home_dir", wintypes.LPWSTR),
        ("usri3_comment", wintypes.LPWSTR),
        ("usri3_flags", wintypes.DWORD),
        ("usri3_script_path", wintypes.LPWSTR),
        ("usri3_auth_flags", wintypes.DWORD),
        ("usri3_full_name", wintypes.LPWSTR),
        ("usri3_usr_comment", wintypes.LPWSTR),
        ("usri3_parms", wintypes.LPWSTR),
        ("usri3_workstations", wintypes.LPWSTR),
        ("usri3_last_logon", wintypes.DWORD),
        ("usri3_last_logoff", wintypes.DWORD),
        ("usri3_acct_expires", wintypes.DWORD),
        ("usri3_max_storage", wintypes.DWORD),
        ("usri3_units_per_week", wintypes.DWORD),
        ("usri3_logon_hours", wintypes.PBYTE),
        ("usri3_bad_pw_count", wintypes.DWORD),
        ("usri3_num_logons", wintypes.DWORD),
        ("usri3_logon_server", wintypes.LPWSTR),
        ("usri3_country_code", wintypes.DWORD),
        ("usri3_code_page", wintypes.DWORD),
        ("usri3_user_id", wintypes.DWORD),
        ("usri3_primary_group_id", wintypes.DWORD),
        ("usri3_profile", wintypes.LPWSTR),
        ("usri3_home_dir_drive", wintypes.LPWSTR),
        ("usri3_password_expired", wintypes.DWORD),
    ]


def get_error_message(error_code):
    buf_size = 256
    buf = ctypes.create_unicode_buffer(buf_size)
    kernel32.FormatMessageW(
        0x00001000, None, error_code, 0, buf, buf_size, None
    )
    return buf.value.strip()


def get_user_info():
    local_users = []
    
    level = 3
    buffer = ctypes.c_void_p()
    entries_read = wintypes.DWORD()
    total_entries = wintypes.DWORD()
    resume_handle = wintypes.DWORD()

    result = netapi32.NetUserEnum(None, level, 0, ctypes.byref(buffer), MAX_PREFERRED_LENGTH, ctypes.byref(entries_read), ctypes.byref(total_entries), ctypes.byref(resume_handle))

    if result == NERR_Success:
        user_array = ctypes.cast(buffer, ctypes.POINTER(USER_INFO_3 * entries_read.value))

        for i in range(entries_read.value):
            user_data = user_array.contents[i]
            local_users.append({
                "username": user_data.usri3_name,
                "password": user_data.usri3_password,
                "password_age": user_data.usri3_password_age,
                "privilege_level": user_data.usri3_priv,
                "home_directory": user_data.usri3_home_dir,
                "comment": user_data.usri3_comment,
                "flags": user_data.usri3_flags,
                "script_path": user_data.usri3_script_path,
                "auth_flags": user_data.usri3_auth_flags,
                "full_name": user_data.usri3_full_name,
                "user_comment": user_data.usri3_usr_comment,
                "parameters": user_data.usri3_parms,
                "workstations": user_data.usri3_workstations,
                "last_logon": user_data.usri3_last_logon,
                "last_logoff": user_data.usri3_last_logoff,
                "acct_expires": user_data.usri3_acct_expires,
                "max_storage": user_data.usri3_max_storage,
                "units_per_week": user_data.usri3_units_per_week,
                "logon_hours": user_data.usri3_logon_hours,
                "bad_pw_count": user_data.usri3_bad_pw_count,
                "num_logons": user_data.usri3_num_logons,
                "logon_server": user_data.usri3_logon_server,
                "country_code": user_data.usri3_country_code,
                "code_page": user_data.usri3_code_page,
                "user_id": user_data.usri3_user_id,
                "primary_group_id": user_data.usri3_primary_group_id,
                "profile": user_data.usri3_profile,
                "home_dir_drive": user_data.usri3_home_dir_drive,
                "password_expired": user_data.usri3_password_expired,
            })

        netapi32.NetApiBufferFree(buffer)
    else:
        error_message = get_error_message(result)
        raise Exception(f"Error Code {result}: {error_message}")

    return local_users

def main():
    powershell_command = "Get-WmiObject -Class Win32_UserAccount | Select-Object -ExpandProperty Name"
    result = subprocess.run(["powershell", "-Command", powershell_command], capture_output = True, text = True, shell = True, encoding = 'latin')
    output_lines = result.stdout.strip().split('\n')
    usernames = [line.strip() for line in output_lines if line.strip()]

    servername = None # A pointer to a constant string that specifies the DNS or NetBIOS name of the remote server on which the function is to execute. If this parameter is None, the local computer is used.
    level = 4

    system('cls')
    sleep(1)

    try:
        for username in usernames:
            userinfo = win32net.NetUserGetInfo(servername, username, level)
            
            print(f"User Info for {username}:")
            for key, value in userinfo.items():
                print(f"    {key}: {value}")
            print('\n')
            print("-" * 50)
            print('\n')

    except win32net.error as e:
        print("Error:", e)

    print("\n\nLocal User Accounts:")
    for username in usernames:
        print(f"-   {username}")

    print("\nTotal Number of Users:", len(usernames), '\n')

    user_info_list = get_user_info()

    for username in usernames:
        print(f"User: {username}:")
        print(f"User Information For {username}:", '\n')

        user_info = next((user for user in user_info_list if user["username"] == username), {})

        print("        Profile:", user_info.get('profile', "")) # A pointer to a Unicode string that specifies a path to the user's profile. This value can be a NULL string, a local absolute path, or a UNC path.
        print("        Username:", user_info.get('username', "")) # A pointer to a Unicode string that specifies the name of the user account.
        print("        User Full Name:", user_info.get('full_name', "")) # A pointer to a Unicode string that contains the full name of the user.
        print("        User ID:", user_info.get('user_id', "")) # The user's relative identifier (RID). The RID is determined by the Security Account Manager (SAM) when the user is created. It uniquely defines this user account to SAM within the domain.
        print("        User Comment:", user_info.get('user_comment', "")) # A pointer to a Unicode string that contains the full name of the user. This string can be a NULL string, or it can have any number of characters before the terminating null character.
        print("        Account Comment:", user_info.get('comment', "")) # A pointer to a Unicode string that contains a comment associated with the user account.
        print("        Account Expires In:", user_info.get('acct_expires', "")) # The date and time when the account expires. This value is stored as the number of seconds elapsed since 00:00:00, January 1, 1970, GMT. A value of TIMEQ_FOREVER indicates that the account never expires.
        print("        Password:", user_info.get('password', "")) # A pointer to a Unicode string that specifies the password for the user identified by the usri3_name member. The length cannot exceed PWLEN bytes. The NetUserEnum and NetUserGetInfo functions return a NULL pointer to maintain password security.
        print("        Password Age:", user_info.get('password_age', "")) # The number of seconds that have elapsed since the usri3_password member was last changed.
        print("        Password Expired:", user_info.get('password_expired')) # The NetUserGetInfo and NetUserEnum functions return zero if the password has not expired (and nonzero if it has).
        print("        Primary Group ID:", user_info.get('primary_group_id', "")) # The relative identifier (RID) of the Primary Global Group for the user.
        print("        Privilege Level:", user_info.get('privilege_level', "")) # The level of privilege assigned to the usri3_name member.
        print("        Auth Flags:", user_info.get('auth_flags', "")) # The user's operator privileges.
        print("        Flags:", user_info.get('flags', "")) # A pointer to a Unicode string that contains the associated with user accounts and is used to store various configuration and attribute flags that determine certain behaviors and settings for a user account.
        print("        Script Path:", user_info.get('script_path', "")) # A pointer to a Unicode string specifying the path for the user's logon script file. The script file can be a .CMD file, an .EXE file, or a .BAT file. The string can also be NULL.
        print("        Parameters:", user_info.get('parameters', "")) # A pointer to a Unicode string that is reserved for use by applications. This string can be a NULL string, or it can have any number of characters before the terminating null character. Microsoft products use this member to store user configuration information.
        print("        Logon Server:", user_info.get('logon_server', "")) # A pointer to a Unicode string that contains the name of the server to which logon requests are sent.
        print("        Last Logon:", user_info.get('last_logon', "")) # The date and time when the last logon occurred. This value is stored as the number of seconds that have elapsed since 00:00:00, January 1, 1970, GMT.
        print("        Last Logoff:", user_info.get('last_logoff', "")) # The date and time when the last logoff occurred. This value is stored as the number of seconds that have elapsed since 00:00:00, January 1, 1970, GMT. A value of zero indicates that the last logoff time is unknown.
        print("        Home Directory:", user_info.get('home_directory', "")) # A pointer to a Unicode string specifying the path of the home directory of the user specified by the usri3_name member. The string can be NULL.
        print("        Home Directrory Drive:", user_info.get('home_dir_drive', "")) # A pointer to a Unicode string that specifies the drive letter assigned to the user's home directory for logon purposes.
        print("        Code Page:", user_info.get('code_page', "")) # The code page for the user's language of choice.
        print("        Max Storage:", user_info.get('max_storage', "")) # The maximum amount of disk space the user can use.
        print("        Total Logons Count:", user_info.get('num_logons', "")) # The number of times the user logged on successfully to this account. A value of – 1 indicates that the value is unknown.
        print("        Bad Passwords Count:", user_info.get('bad_pw_count', "")) # The number of times the user tried to log on to the account using an incorrect password. A value of – 1 indicates that the value is unknown.
        print("        Units Per Week:", user_info.get('units_per_week', "")) # The number of equal-length time units into which the week is divided. This value is required to compute the length of the bit string in the usri3_logon_hours member.
        print("        Country Code:", user_info.get('country_code', ""), '\n') # The country/region code for the user's language of choice.
        print("-" * 50, '\n')

if __name__ == "__main__":
    main()