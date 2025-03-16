from libs.account.msa import *
from libs.account.mojang_api import *
from libs.account.yggdrasil import *


def get_access_token_msa(msa_auth_code, refresh_code=False):
    code_type = "RefreshToken" if refresh_code else "AccessToken"
    msa_tk_status, microsoft_token, microsoft_refresh_token, err = get_microsoft_account_token(msa_auth_code, code_type)
    if not msa_auth_code:
        return False, None, None, None, f"GetMicrosoftAccToken>{err}"

    xbl_tk_status, xbl_token, err = get_xbl_token(microsoft_token)
    if not xbl_tk_status:
        return False, None, None, None, f"GetXblToken>{err}"

    xsts_tk_status, xsts_userhash, xsts_token = get_xsts_token(xbl_token)
    if not xsts_token:
        return False, None, None, None, f"GetXstsToken>{err}"

    access_tk_status, access_token = get_access_token(xsts_userhash, xsts_token)
    if not access_tk_status:
        return False, None, None, None, f"GetAccessToken>{err}"

    return True, access_token

# If you want to get accessToken using yggdrasil api. Using get_access_token_yggdrasil (from ibs.account.yggdrasil)
