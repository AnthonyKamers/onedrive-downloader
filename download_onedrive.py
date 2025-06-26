import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv


def baixar_arquivos_onedrive(url, download_dir):
    load_dotenv()
    is_docker = os.getenv("IS_DOCKER") == "True"

    if is_docker:
        options = Options()
    else:
        options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")  # Remova esta linha para ver a ‘interface’
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")


    experimental_options = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option('prefs', experimental_options)

    # Iniciar driver
    if is_docker:
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
    else:
        print("aqui")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Abrir link público do OneDrive
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ms-List-cell"))
        )

        # Encontrar os links de download (pode variar conforme layout da Microsoft)
        file_elements = driver.find_elements(By.CSS_SELECTOR, ".ms-List-cell")

        print(f"{len(file_elements)} arquivos encontrados.")

        for file in file_elements:
            file.click()
            sleep(1)

            # button download
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@name='Download']"))
            )
            download_button.click()
            sleep(5)
    finally:
        driver.quit()

    return [os.path.join(download_dir, f) for f in os.listdir(download_dir)]


if __name__ == "__main__":
    URL_TEST = 'https://1drv.ms/u/s!AsVxlxsTVsQrguQVzHVFKcF89upVDg?e=IrdIbC'
    baixar_arquivos_onedrive(URL_TEST, "/tmp")
