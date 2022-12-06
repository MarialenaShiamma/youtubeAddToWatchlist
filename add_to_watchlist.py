# import required libraries
import os
import re
import datetime
from time import sleep, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import undetected_chromedriver.v2 as uc


class YoutubeList():

    # initialise the script
    def __init__(self):

        # # specify selenium driver (chromedriver) - traceable driver by google
        # # opts = Options()
        # # opts.add_argument("--start-maximized")
        # # opts.add_argument("--headless")
        # # opts.add_argument('--disable-gpu')
        # # opts.add_argument('window-size=100x100')
        # # opts.add_argument("user-data-dir=C:\\Users\\MShiamma\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
        # # opts.set_headless() # this will keep the browser closed when the script will be executed
        # # self.browser = Chrome(options=opts)

        # not traceable driver by google
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user_agent=DN")

        # should add latest version of chrome here
        self.browser = uc.Chrome(options=chrome_options, version_main=108)
        self.browser.delete_all_cookies()

        self.browser.get('http://youtube.com')

        # Sleep to give the browser time to render and finish any animations
        sleep(6)

        # Close popup that may open right after you open youtube for the first time
        login_or_not = False
        try:
            # old popup
            # self.browser.find_element_by_class_name("ytd-popup-container")
            # self.browser.find_element_by_css_selector("#action-button > yt-button-renderer").click()

            # new popup about cookies
            login_button = self.browser.find_elements_by_xpath(
                "//ytd-button-renderer[contains(@class,'signin')]")[1]
            login_button.click()
            login_or_not = True

        except Exception:
            pass

        # sign in
        self.login(login_or_not)

        i = 0
        while i < 2:
            # add videos in watchlist
            self.add_to_watchlist()

            # self.browser.refresh()
            self.browser.get('http://youtube.com')

            sleep(6)
            i = i+1

        # quit browser
        self.browser.quit()

    # login to YouTube

    def login(self, login_or_not):

        # skip login click if already clicked
        if not login_or_not:
            sleep(2)

            # locate the login button
            # login_button = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Sign in']")))
            login_button = self.browser.find_elements_by_css_selector(
                "tp-yt-paper-button")[9]  # signin is the 9th element
            login_button.click()

            sleep(2)

        # get email and set to email input box
        email = self.browser.find_element_by_id("identifierId")
        myemail = os.environ.get('YOUTUBE_EMAIL')
        email.send_keys(myemail)
        sleep(2)

        # click next button
        email_next_button = self.browser.find_element_by_id("identifierNext")
        email_next_button.click()

        sleep(2)

        # get password and set to password input box
        password = self.browser.find_element_by_name("Passwd")
        mypassword = os.environ.get('YOUTUBE_PASSWORD')
        password.send_keys(mypassword)
        sleep(2)

        # click next button to log in
        pass_next_button = self.browser.find_element_by_id("passwordNext")
        pass_next_button.click()
        sleep(20)

        # try:
        #     # confirm phone if appears otherwise proceed
        #     self.browser.find_element_by_xpath(
        #         "//*[contains(text(),'Confirm')]").click()
        #     sleep(3)
        # except:
        #     pass

    # add unwatched videos to watchlist

    def add_to_watchlist(self):

        # # open show more section
        # try:

        #     more = self.browser.find_elements_by_xpath(
        #         "//paper-button[@aria-label='Show more']")
        #     for m in more:

        #         m.click()
        #         sleep(3)
        # except:

        #     pass

        # scroll until there are no more videos in the homepage of youtube
        # homepage is around 20-30 scrolls from the bottom of the page
        # tried to check for the loader that appears with every scroll to avoid using the hardcoded value, but the loader does not always appear in decent networks
        i = 0
        while i <= 30:

            try:

                # scroll to the end of the page
                self.browser.find_element_by_tag_name(
                    'body').send_keys(Keys.END)
                act = ActionChains(self.browser)
                act.send_keys(Keys.PAGE_DOWN).perform()

                # allow some time for the videos to get loaded
                sleep(0.5)

                # proceed to next page with videos
                i = i + 1
            except:

                continue

        self.browser.find_element_by_tag_name('body').send_keys(
            Keys.CONTROL + Keys.HOME)  # go at the top of the page

        self.logic()  # call logic before scrolling

    def logic(self):
        # set time format
        FMT = '%H:%M:%S'

        # get all video containers
        videos = self.browser.find_elements_by_tag_name(
            "ytd-rich-grid-media")

        # loop all videos
        for v in videos:

            try:

                # get time of the video
                time_vid = v.find_element_by_css_selector(
                    "#overlays > ytd-thumbnail-overlay-time-status-renderer > span")

                try:

                    # some times have hours as well
                    time_vid_hour = time_vid.text.split(':')[0]
                    time_vid_min = time_vid.text.split(':')[1]
                    time_vid_sec = time_vid.text.split(':')[2]

                    a = datetime.time(int(time_vid_hour), int(
                        time_vid_min), int(time_vid_sec))
                except IndexError:

                    try:

                        # for times that are less than an hour
                        time_vid_min = time_vid.text.split(':')[0]
                        time_vid_sec = time_vid.text.split(':')[1]

                        # print("min sec " + time_vid_min + ':' + time_vid_sec  + '\n')

                        a = datetime.time(
                            0, int(time_vid_min), int(time_vid_sec))

                    except IndexError:

                        continue

                # check if video is between 2 and 6 minutes
                if a < datetime.time(0, 6, 0) and a > datetime.time(0, 2, 0):

                    # extract video title and entertainment company
                    video_title = v.find_element_by_id(
                        "video-title").text
                    video_company_title = v.find_element_by_id(
                        "channel-name").text

                    # words we dont want to be included in title / company
                    unwanted_text = ['delicious day', 'reaction', 'netflix', 'traveler', 'tv', 'news', 'mbclife', 'top daily', 'chosun', 'gems', 'kbs entertain', 'mbcentertainment', 'sbs', '1thek official', 'ytn', 'jtbc', 'trailer', 'music bank', 'mcountdown',
                                     'making film', 'cook', 'kitchen', 'table diary', 'vlog', 'asmr', 'clip', 'teaser', 'medley', 'ep.', 'running man', '[hot]', 'behind the scene', 'performance', 'practice', 'cam', 'instrumental', 'backstage', 'choreography', 'preview', 'inkigayo', 'dance cover']

                    # check if it contains korean characters and doesnt contain the words:
                    if (any([re.search(u'[\u3131-\ucb4c]', x) for x in video_title]) or any([re.search(u'[\u3131-\ucb4c]', x) for x in video_company_title])) and not (any(x in video_title.lower() for x in unwanted_text) or any(x in video_company_title.lower() for x in unwanted_text)):

                        # print("GOOD: Acceptable title and company - " + video_title.lower() + " / " + video_company_title.lower())

                        # check if already watched
                        try:

                            v.find_element_by_id('progress')
                            continue
                        except Exception:
                            pass

                        # scroll to details section of video
                        move = ActionChains(self.browser).move_to_element(
                            v.find_element_by_tag_name("ytd-video-meta-block"))
                        move.perform()
                        sleep(2)

                        # # hover on element
                        # hover = ActionChains(
                        #     self.browser).move_to_element(v.find_element_by_tag_name("ytd-thumbnail"))
                        # hover.perform()
                        # sleep(6)

                        # check if already in watchlist
                        # try:

                        #     v.find_element_by_xpath(
                        #         "//ytd-thumbnail-overlay-toggle-button-renderer[contains(@aria-label, 'Added')]")
                        #     #print("already in watchlist\n")
                        #     continue
                        # except Exception:

                        # print("Name korean -" + video_title + " OR " + video_company_title)
                        # print("Time looks ok - " + str(time_vid) + '\n')

                        try:

                            # add video in watchlist
                            # v.find_element_by_xpath(
                            #     "//button[@aria-label='Action menu']").click()
                            v.find_element_by_tag_name(
                                "ytd-menu-renderer").click()

                            sleep(2)

                            v.find_element_by_xpath(
                                "//yt-formatted-string[normalize-space()='Save to Watch later']").click()
                            # v.find_element_by_xpath("//span[contains(text(),'Watch later')]").click()

                            # wait before proceeding
                            sleep(1)
                        except:

                            continue
                    else:

                        # print("BAD: no korean or not acceptable name - " + video_title + " / " + video_company_title + "\n")
                        continue
                else:

                    #print("wrong time\n")
                    continue
            except:

                continue


# main
if __name__ == "__main__":

    YoutubeList().__init__()
