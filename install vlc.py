import requests
import hashlib
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_expected_sha256(url):
    """
    Get the expected SHA-256 hash value of the VLC installer from the provided URL.
    """
    try:
        resp_msg = requests.get(url)
        resp_msg.raise_for_status()  # Raise an HTTPError for bad responses
        logging.info(f"Response from SHA-256 URL: {resp_msg.text}")
        return resp_msg.text.split()[0]
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve the expected SHA-256 hash value: {e}")
        raise

def download_installer(url):
    """
    Download the VLC installer from the provided URL.
    """
    try:
        resp_msg = requests.get(url)
        resp_msg.raise_for_status()  # Raise an HTTPError for bad responses
        return resp_msg.content
    except requests.RequestException as e:
        logging.error(f"Failed to download the VLC installer: {e}")
        raise

def installer_ok(installer_data, expected_sha256):
    """
    Verify the integrity of the downloaded VLC installer by comparing the
    expected and computed SHA-256 hash values.
    """
    computed_sha256 = hashlib.sha256(installer_data).hexdigest()
    if computed_sha256 == expected_sha256:
        logging.info("Installer integrity verified.")
        return True
    else:
        logging.warning("The downloaded installer is corrupted.")
        return False

def save_installer(installer_data):
    """
    Save the downloaded VLC installer to disk.
    """
    home_dir = os.path.expanduser('~')  # User's home directory
    installer_path = os.path.join(home_dir, 'vlc_installer.exe')
    try:
        with open(installer_path, 'wb') as file:
            file.write(installer_data)
        logging.info(f"Installer saved to {installer_path}.")
        return installer_path
    except OSError as e:
        logging.error(f"Failed to save the installer: {e}")
        raise

# You can skip or comment out the actual installation step
def run_installer(installer_path):
    """
    Silently run the VLC installer.
    """
    logging.info(f"Simulating installation of {installer_path}. (Installation skipped)")
    # Uncomment the lines below to perform actual installation
    # try:
    #     subprocess.run([installer_path, '/L=1033', '/S'], check=True)
    #     logging.info("VLC Media Player installed successfully.")
    # except subprocess.CalledProcessError as e:
    #     logging.error(f"Failed to run the installer: {e}")
    #     raise

def delete_installer(installer_path):
    """
    Delete the VLC installer from disk.
    """
    try:
        os.remove(installer_path)
        logging.info(f"Installer deleted from {installer_path}.")
    except OSError as e:
        logging.error(f"Failed to delete the installer: {e}")
        raise

def main():
    hash_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    installer_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    
    try:
        logging.info("Starting the VLC installer download and installation process.")
        expected_sha256 = get_expected_sha256(hash_url)
        installer_data = download_installer(installer_url)
        
        if installer_ok(installer_data, expected_sha256):
            installer_path = save_installer(installer_data)
            run_installer(installer_path)  # Comment out this line to skip installation
            delete_installer(installer_path)
        else:
            logging.error("Installation aborted due to installer corruption.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
