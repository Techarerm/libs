"""
AccountData(v3):
[
    {
        "id": 1,  # For account management
        "Username": "Player",
        "UUID": "Unknown",
        "RefreshToken": "None",
        "AccessToken": "Unknown",
        "tag": "TempUser;DemoUser", # Unused
        "AccountType": "msa", # Account type (msa = Microsoft Account, mojang = Yggdrasil(Not working),
        legacy = Legacy authentication(Not working), offline = (DEBUG ONLY)
    },
    {
        "id": 2,
        "Username": "TedKai", # Your username
        "UUID": "576477ee9099488798f478d81e6f9fae", # Your Minecraft Account UUID
        "RefreshToken": "Example RefreshToken", # Your Microsoft Account Refresh Token(it use on refresh token)
        "AccessToken": "Example AccessToken", # Your Minecraft Account Token(Or session token. Expire in one day)
        "AccountType": "msa"
    }
]
"""
import json
import os

account_data_sample = {
}


def create_account_data(account_data_path, overwrite=False):
    """
    Create AccountData (if the file exists set overwrite=True)
    :param account_data_path: Account data path (AccountData.json)
    :param overwrite: Overwrite existing account data if it exists
    :return: Status
    """
    if os.path.exists(account_data_path) and not overwrite:
        return False

    try:
        with open(account_data_path, 'w') as f:
            json.dump(account_data_sample, f)
        f.close()
    except Exception as e:
        print("[DEBUG] Unable to write account_data_sample to AccountData. ERR:{}".format(e))
        return False

    return True


def read_account_data(account_data_path):
    """
    Read AccountData
    :param account_data_path: Account data path (AccountData.json)
    :return: Status, AccountData, ErrorMEssage
    """
    if not os.path.exists(account_data_path):
        return False, None, "Target AccountData does not exist"

    try:
        with open(account_data_path, 'r') as f:
            return True, json.load(f), None
    except Exception as e:
        return False, None, "Unable to read AccountData. ERR:{}".format(e)


def get_new_account_id(account_data_path):
    """
    Get new account ID
    :param: account_data_path: Account data path (AccountData.json)
    :return: new_account_id: int, ErrorMessage
    """

    try:
        with open(account_data_path, 'r') as f:
            account_data = json.load(f)
    except Exception as e:
        return False, e

    # Get all id inside the AccountData
    ids = [entry['id'] for entry in account_data]
    new_id = 1
    while new_id in ids:
        # If id 1 is in data, new_id + 1 until can't find same one.
        new_id += 1

    return new_id, None


def rearrange_all_accounts(account_data_path):
    """
    Rearrange all accounts ID
    :param: account_data_path: Account data path (AccountData.json)
    :return: Status, ErrorMessage
    """

    try:
        with open(account_data_path, 'r') as f:
            account_data = json.load(f)
    except Exception as e:
        return False, e

    account_id_count = 1 + len(account_data)

    for new_account_id, account_data in zip(range(account_id_count), account_data):
        account_data["id"] = new_account_id

    try:
        with open(account_data_path, 'w') as f:
            json.dump(account_data, f)
    except Exception as e:
        return False, e

    return True, None


def write_new_account_to_account_data(account_data_path, account_name, uuid, refresh_token, access_token, account_type,
                                      tag=""):
    """
    Write the new account_data
    :param account_data_path: Account data path (AccountData.json)
    :param account_name: Account name
    :param uuid: Account UUID
    :param refresh_token: Refresh token
    :param access_token: Access token
    :param account_type: Account type
    :param tag: Account tag
    :return: Status, ErrorMessage
    """
    new_account_id = get_new_account_id(account_data_path)

    new_account_data = {
        "id": new_account_id,
        "Username": account_name,
        "UUID": uuid,
        "RefreshToken": refresh_token,
        "AccessToken": access_token,
        "AccountType": account_type,
        "tag": tag
    }

    try:
        with open(account_data_path, 'r') as f:
            AccountData = json.load(f, encoding='utf-8')
    except Exception as e:
        return False, e

    AccountData.append(new_account_data)

    try:
        with open(account_data_path, 'w') as f:
            json.dump(AccountData, f, indent=4)
    except Exception as e:
        return False, e, None

    return True, new_account_id, None


def check_target_account_exists_using_uuid(account_data_path, uuid):
    """
    Check if the target account exists
    :param account_data_path: AccountData path (AccountData.json)
    :param uuid: Account UUID
    :return: account_exists_status, exists_account_id, ErrorMessage
    """
    status, AccountData = read_account_data(account_data_path)

    if not status:
        return False, "Target AccountData does not exist"

    existing_entry = next((entry for entry in AccountData if entry["UUID"] == uuid), None)

    if existing_entry:
        return True, existing_entry["id"], None

    return False, None, "Target AccountData does not exist"


def get_account_data_use_account_id(account_data_path, target_id):
    """
    Get account data (subitem) from AccountData
    :param account_data_path: Account data path (AccountData.json)
    :param target_id: Target account ID
    :return: Status, AccountData, ErrorMessage
    """
    if os.path.exists(account_data_path):
        with open(account_data_path, 'r') as f:
            try:
                json_data = json.load(f)
                # Loop through the data and find the matching ID
                for entry in json_data:
                    if entry['id'] == int(target_id):
                        # Return the matching entry
                        return True, entry, None
                return False, None, "Target ID not found."
            except Exception as e:
                return False, None, e
    else:
        return False, None, "Specified AccountData file does not exist."


def get_account_info_from_account_data(account_data_path, target_id):
    """
    Get account data by account ID
    :param account_data_path: Account data path (AccountData.json)
    :param target_id: The target account ID
    :return: Status, username, UUID, ErrorMessage
    """
    Status, accData, e = get_account_data_use_account_id(account_data_path, target_id)

    if Status:
        accName = accData.get("Username", None)
        accUUID = accData.get("UUID", None)
        return True, accName, accUUID, None
    else:
        return False, None, None, e


def update_specified_account_data(account_data_path, target_account_id, username, refresh_token, access_token):
    """
    Update specified account data from AccountData
    :param account_data_path: Account data path (AccountData.json)
    :param target_account_id: Target account ID
    :param username: Minecraft username
    :param refresh_token: Refresh token
    :param access_token: Access token
    :return: Status, ErrorMessage
    """
    # Convert target id to integer
    if type(target_account_id) != int:
        try:
            target_account_id = int(target_account_id)
        except Exception as e:
            return False, "Updating target account data failed while convert target id to integer. ERR:{}".format(e)

    # Load JSON data
    status, AccountData, e = read_account_data(account_data_path)
    if not status:
        return False, f"Updating target account data failed: {e} | Get main AccountData data failed."

    # Update "select" account data
    account_found = False
    try:
        for account in AccountData:
            if account['id'] == target_account_id:  # Fixed: Using account_id
                account['Username'] = username  # Update if username changed
                account["RefreshToken"] = refresh_token
                account["AccessToken"] = access_token
                account_found = True
                break
    except Exception as e:
        return False, "Updating target account data failed while replacing old information. ERR:{}".format(e)

    # Write back to the AccountData if the target account was found and updated
    if account_found:
        try:
            with open(account_data_path, "w") as jsonFile:
                json.dump(AccountData, jsonFile, indent=4)
            return True, None
        except IOError as e:
            return False, f"Updating target account data failed while writing back account data. ERR:{e}."

    return False, f"Target account ID {target_account_id} not found."
