import os
import subprocess
import time
import shutil


def clear_chrome_data():
    # Find and kill all Chrome processes
    subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for Chrome processes to terminate
    time.sleep(5)

    # Clear Chrome cookies and cache for the current user
    localappdata_path = os.environ.get('LOCALAPPDATA')
    chrome_user_path = os.path.join(localappdata_path, 'Google', 'Chrome', 'User Data')
    chrome_cookies_path = os.path.join(chrome_user_path, 'Default', 'Cookies')
    chrome_cache_path = os.path.join(chrome_user_path, 'Default', 'Cache')

    # Delete cookies file
    if os.path.exists(chrome_cookies_path):
        os.remove(chrome_cookies_path)

    # Delete cache files
    if os.path.exists(chrome_cache_path):
        shutil.rmtree(chrome_cache_path)


def clear_edge_data():
    # Find and kill all Chrome processes
    subprocess.run(['taskkill', '/F', '/IM', 'msedge.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for Chrome processes to terminate
    time.sleep(5)

    # Clear Chrome cookies and cache for the current user
    localappdata_path = os.environ.get('LOCALAPPDATA')
    edge_user_path = os.path.join(localappdata_path, 'Microsoft', 'Edge', 'User Data')
    edge_cookies_path = os.path.join(edge_user_path, 'Default', 'Cookies')
    edge_cache_path = os.path.join(edge_user_path, 'Default', 'Cache')

    # Delete cookies file
    if os.path.exists(edge_cookies_path):
        os.remove(edge_cookies_path)

    # Delete cache files
    if os.path.exists(edge_cache_path):
        shutil.rmtree(edge_cache_path)


def clear_firefox_data():
    # kill firefox processes
    subprocess.run(['taskkill', '/F', '/IM', 'firefox.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for Chrome processes to terminate
    time.sleep(5)

    # Clear Cookies
    appdata_path = os.environ.get('APPDATA')
    firefox_user_rpath = os.path.join(appdata_path, 'Mozilla', 'Firefox', 'Profiles')
    if os.path.exists(firefox_user_rpath):
        x = os.listdir(firefox_user_rpath)
        for i in x:
            firefox_cookies_path = os.path.join(firefox_user_rpath, f'{i}', 'cookies.sqlite')
            if os.path.exists(firefox_cookies_path):
                shutil.rmtree(firefox_cookies_path)

    # Clear Caches
    localappdata_path = os.environ.get('LOCALAPPDATA')
    firefox_user_path = os.path.join(localappdata_path, 'Mozilla', 'Firefox', 'Profiles')
    if os.path.exists(firefox_user_path):
        y = os.listdir(firefox_user_path)
        for j in y:
            firefox_caches_path = os.path.join(firefox_user_path, f'{j}', 'cache2')
            if os.path.exists(firefox_caches_path):
                shutil.rmtree(firefox_caches_path)


if __name__ == "__main__":
    clear_chrome_data()
    clear_edge_data()
    clear_firefox_data()
