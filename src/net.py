import chromedriver_autoinstaller
from screeninfo import get_monitors
from selenium import webdriver


def start_browser(url):
    size_x = 1050
    size_y = 600
    monitors = get_monitors()
    screen_height = monitors[0].height
    screen_width = monitors[0].width
    location_x = int(screen_width / 2) - int(size_x / 2)
    location_y = int(screen_height / 2) - int(size_y / 2)
    chromedriver_autoinstaller.install(cwd=True)
    options = webdriver.ChromeOptions()
    options.add_argument(f"--app={url}")
    options.add_argument("--incognito")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(f"window-size={size_x},{size_y}")
    options.add_argument(f"window-position={location_x},{location_y}")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
