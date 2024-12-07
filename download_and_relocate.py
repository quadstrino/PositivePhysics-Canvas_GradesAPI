# Automate downloading of grades from PositivePhysics.org
def download(units, directory_path):
    """
    This function uses Playwright to simulate a browser interaction with PositivePhysics.org
    and download the completion scores for the specified units. It will create a temporary 
    directory to download the scores to and then move the downloaded files to the correct 
    directory, deleting any previously downloaded files for the specified units.

    Args:
    
        units (list): List of unit names to download scores for.
        directory_path (str): Path to the directory containing the configuration file and where the downloaded
            scores will be saved.

    Returns:
        None
    """
    
    from playwright.sync_api import sync_playwright
    from datetime import datetime
    import os
    import glob
    import pandas as pd
    from natsort import natsorted
    import tempfile

    today = datetime.now().strftime("%Y-%m-%d(%H-%M-%S)")
    try:
        os.mkdir(rf"{directory_path}\downloads")
    except:
        pass
    downloads_dir = rf"{directory_path}\downloads"
    temp_dir = tempfile.TemporaryDirectory(dir=downloads_dir)
    temp_download_path = rf"{temp_dir.name}"

    with open(rf"{directory_path}\config.txt") as f:
        lines = f.readlines()
        username = lines[2].strip()
        password = lines[4].strip()
        classcode = lines[6].strip()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, downloads_path=temp_download_path)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://www.positivephysics.org/")

        # Define elements for positivephysics.org and login
        page.click("#signinButton")
        page.fill("#loginUsername", username)
        page.fill("#loginPassword", password) 
        page.fill("#loginClassCode", classcode)
        page.click("#loginButton")

        page.wait_for_selector('xpath=/html/body/div[1]/div[3]/nav/div[4]/ul[2]/li[3]/a/span')

        # Import URLs for score pages from +Phys
        scores_urls = pd.read_csv(rf"{directory_path}\posphys_urls.csv")

        # Navigate to and download scores
        for index, row in scores_urls.iterrows():
            if row['unit_name'] in units:
                
                print(f"Downloading scores for {row['unit_name']}...")
                page.goto(row['url'])
                page.wait_for_function(
                    "document.querySelector('#pageContent > div.container-fluid.pl-4.pr-4.pt-1.pb-6 table tbody')"
                    " && document.querySelectorAll('#pageContent > div.container-fluid.pl-4.pr-4.pt-1.pb-6 table tbody tr').length > 10"
                )
                
                # Click the export button to download scores
                with page.expect_download() as download_info:
                    page.click("#exportButton")  # Trigger download

                # Rename downloaded file (also check if file already exists)
                download = download_info.value
                if os.path.exists(os.path.join(temp_download_path, f"{row['unit_name']+"_"+today}")):
                    os.remove(os.path.join(temp_download_path, f"{row['unit_name']+"_"+today}"))
                os.rename(download.path(), os.path.join(temp_download_path, f"{row['unit_name']+"_"+today}"))

        # Close browser and update UI
        browser.close()

    # move new files to correct directory
    for fname in os.listdir(temp_download_path):
        if today in fname:
            old_path = temp_download_path + "\\" + fname
            new_path = downloads_dir + "\\" + fname
            os.replace(old_path, new_path)

    # delete old files
    file_list = []
    for file in list(glob.glob('unit*',root_dir=downloads_dir)):
        file_list.append(file.split("_")[:1][0])

    for unit in natsorted(set(file_list)):
        repeats = []
        for file in list(glob.glob(unit+'_*', root_dir=downloads_dir)):
            repeats.append(file)
        for thing in natsorted(repeats):
            if thing == natsorted(repeats)[-1]:
                continue
            else:
                os.remove(downloads_dir + "\\" + thing)

    temp_dir.cleanup()
