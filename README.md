# Get user information with DLLs provided by the Windows API
* This script retrieves highly detailed user information using with **`advapi32`**, **`netapi32`** and **`kernel32`** DLLs.

# INSTALLATION
```bash
pip install -r requirements.txt
```
# A quick look at what the code is doing

* If you want to take a quick look at what the code is doing, you can use the code below.

```py
from win32net import NetUserEnum, NetUserGetInfo
from win32netcon import FILTER_NORMAL_ACCOUNT

servername = None # A pointer to a constant string that specifies the DNS or NetBIOS name of the remote server on which the function is to execute. If this parameter is None, the local computer is used.
level = 4
resume = 0
users = []

while True:
    users_info, total, resume = NetUserEnum(servername, 0, FILTER_NORMAL_ACCOUNT, resume)
    users.extend([user['name'] for user in users_info])
    if not resume:
        break

for username in users:
    userinfo = NetUserGetInfo(servername, username, level)

    print(f"User Info for {username}:")
    for key, value in userinfo.items():
        print(f"    {key}: {value}")
    print('\n', "-" * 50, '\n')
```
# Below you can see the information the Script gets for each user on your local computer:

* ***Profile*** -  A pointer to a Unicode string that specifies a path to the user's profile. This value can be a NULL string, a local absolute path, or a UNC path.
* ***Username*** - A pointer to a Unicode string that specifies the name of the user account.
* ***User Full Name*** - A pointer to a Unicode string that contains the full name of the user.
* ***User ID*** - The user's relative identifier (RID). The RID is determined by the Security Account Manager (SAM) when the user is created. It uniquely defines this user account to SAM within the domain.
* ***User SID*** - A unique ID number that a computer or domain controller uses to identify you. It is a string of alphanumeric characters assigned to each user on a Windows computer, or to each user, group, and computer on a domain-controlled network such as Indiana University's Active Directory
* ***User Comment*** - A pointer to a Unicode string that contains the full name of the user. This string can be a NULL string, or it can have any number of characters before the terminating null character.
* ***Account Comment*** - A pointer to a Unicode string that contains a comment associated with the user account.
* ***Account Expires In*** - The date and time when the account expires. This value is stored as the number of seconds elapsed since 00:00:00, January 1, 1970, GMT. A value of TIMEQ_FOREVER indicates that the account never expires.
* ***Password*** - A pointer to a Unicode string that specifies the password for the user identified by the usri3_name member. The length cannot exceed PWLEN bytes. The NetUserEnum and NetUserGetInfo functions return a NULL pointer to maintain password security.
* ***Password Age*** - The number of seconds that have elapsed since the usri3_password member was last changed.
* ***Password Expired*** - The NetUserGetInfo and NetUserEnum functions return zero if the password has not expired (and nonzero if it has).
* ***Primary Group ID*** - The relative identifier (RID) of the Primary Global Group for the user.
* ***Privilege Level*** - The level of privilege assigned to the usri3_name member.
* ***Auth Flags*** - The user's operator privileges.
* ***Flags*** - A pointer to a Unicode string that contains the associated with user accounts and is used to store various configuration and attribute flags that determine certain behaviors and settings for a user account.
* ***Script Path*** - A pointer to a Unicode string specifying the path for the user's logon script file. The script file can be a .CMD file, an .EXE file, or a .BAT file. The string can also be NULL.
* ***Parameters*** - A pointer to a Unicode string that is reserved for use by applications. This string can be a NULL string, or it can have any number of characters before the terminating null character. Microsoft products use this member to store user configuration information.
* ***Logon Server*** - A pointer to a Unicode string that contains the name of the server to which logon requests are sent.
* ***Logon Hours*** - A pointer to a 21-byte (168 bits) bit string that specifies the times during which the user can log on. Each bit represents a unique hour in the week, in Greenwich Mean Time (GMT).
* ***Last Logon*** - The date and time when the last logon occurred. This value is stored as the number of seconds that have elapsed since 00:00:00, January 1, 1970, GMT.
* ***Last Logoff*** - The date and time when the last logoff occurred. This value is stored as the number of seconds that have elapsed since 00:00:00, January 1, 1970, GMT. A value of zero indicates that the last logoff time is unknown.
* ***Home Directory*** - A pointer to a Unicode string specifying the path of the home directory of the user specified by the usri3_name member. The string can be NULL.
* ***Home Directrory Drive*** - A pointer to a Unicode string that specifies the drive letter assigned to the user's home directory for logon purposes.
* ***Code Page*** - The code page for the user's language of choice.
* ***Max Storage*** - The maximum amount of disk space the user can use.
* ***Total Logons Count*** - The number of times the user logged on successfully to this account. A value of – 1 indicates that the value is unknown.
* ***Bad Passwords Count*** - The number of times the user tried to log on to the account using an incorrect password. A value of – 1 indicates that the value is unknown.
* ***Units Per Week*** - The number of equal-length time units into which the week is divided. This value is required to compute the length of the bit string in the usri3_logon_hours member.
* ***Country Code*** - The country/region code for the user's language of choice.

* **If you want to learn more about Win32api, you can also check out [this link](https://learn.microsoft.com/en-us/windows/win32/api/lmaccess/)**.
