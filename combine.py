import os
import sqlite3
import json
import csv
from datetime import datetime, timezone


def fetch_firefox_profiles():
    profiles_dir = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
    profiles = [profile for profile in os.listdir(profiles_dir) if os.path.isdir(os.path.join(profiles_dir, profile))]
    return profiles


def export_history_to_csv(profile_path, output_path):
    history_db_path = os.path.join(profile_path, 'places.sqlite')

    if not os.path.exists(history_db_path):
        print(f"History database not found for profile at '{profile_path}'. Skipping.")
        return

    connection = sqlite3.connect(history_db_path)
    cursor = connection.cursor()

    query = """
        SELECT moz_historyvisits.visit_date,
               moz_places.url,
               moz_places.title
        FROM moz_historyvisits
        JOIN moz_places ON moz_historyvisits.place_id = moz_places.id
        ORDER BY moz_historyvisits.visit_date;
    """

    cursor.execute(query)
    history_data = cursor.fetchall()

    csv_path = os.path.join(output_path, f"{os.path.basename(profile_path)}_history.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Visit Time (UTC)', 'URL', 'Title'])

        for visit_date, url, title in history_data:
            utc_visit_time = datetime.fromtimestamp(visit_date / 1000000, tz=timezone.utc)
            csv_writer.writerow([utc_visit_time.strftime('%Y-%m-%d %H:%M:%S'), url, title])

    connection.close()
    print(f"History exported for profile '{profile_path}' to '{csv_path}'.")


def fetch_installed_extensions(profile_path):
    extensions_file_path = os.path.join(profile_path, 'extensions.json')
    installed_extensions = []

    if not os.path.exists(extensions_file_path):
        return installed_extensions

    with open(extensions_file_path, 'r', encoding='utf-8') as extensions_file:
        extensions_data = json.load(extensions_file)

        for extension_info in extensions_data.get('addons', []):
            if extension_info.get('type') == 'extension':
                installed_extensions.append({
                    'Name': extension_info.get('name', ''),
                    'Version': extension_info.get('version', ''),
                    'ID': extension_info.get('id', ''),
                    'Install Time (UTC)': format_install_time(extension_info.get('installDate', 0))
                })

    return installed_extensions


def format_install_time(timestamp):
    install_time = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
    return install_time.strftime('%Y-%m-%d %H:%M:%S')


def export_installed_extensions_to_csv(profile_path, output_path, extensions):
    if not extensions:
        print(f"No installed extensions found for profile at '{profile_path}'.")
        return

    csv_path = os.path.join(output_path, f"{os.path.basename(profile_path)}_installed_extensions.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name', 'Version', 'ID', 'Install Time (UTC)'])

        for extension in extensions:
            csv_writer.writerow(
                [extension['Name'], extension['Version'], extension['ID'], extension['Install Time (UTC)']])

    print(f"Installed extensions exported for profile '{profile_path}' to '{csv_path}'.")


if __name__ == '__main__':
    output_directory = 'C:/windows/Temp/fire_temp/firefox_history_csv'
    output_directory1 = 'C:/windows/Temp/fire_temp/firefox_installed_extensions_csv'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    profiles = fetch_firefox_profiles()

    for profile in profiles:
        profile_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles', profile)
        export_history_to_csv(profile_path, output_directory)

    if not os.path.exists(output_directory1):
        os.makedirs(output_directory1)

    profiles = fetch_firefox_profiles()

    for profile in profiles:
        profile_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles', profile)
        extensions = fetch_installed_extensions(profile_path)
        export_installed_extensions_to_csv(profile_path, output_directory1, extensions)

