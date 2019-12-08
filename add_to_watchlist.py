# import required libraries
import os
import re
import datetime
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class YoutubeList():

    # initialise the script
    def __init__(self):

        #  specify selenium driver - in a similar way you can use firefox
        opts = Options()
        opts.add_argument("--start-maximized")
        # opts.set_headless() # this will keep the browser closed when the script will be executed
        self.browser = Chrome(options=opts)
        self.browser.get('http://youtube.com')

        # Sleep to give the browser time to render and finish any animations
        sleep(2)

        # sign in
        self.login()

        # add videos in watchlist
        self.add_to_watchlist()

        # quit browser
        self.browser.quit()

    # login to YouTube
    def login(self):

        # locate the login button
        login_button = self.browser.find_element_by_xpath(
            "//paper-button[@aria-label='Sign in']")
        login_button.click()

        sleep(2)

        # get email and set to email input box
        email = self.browser.find_element_by_id("identifierId")
        myemail = os.environ.get('YOUTUBE_EMAIL')
        email.send_keys(myemail)

        # click next button
        email_next_button = self.browser.find_element_by_id("identifierNext")
        email_next_button.click()

        sleep(2)

        # get password and set to password input box
        password = self.browser.find_element_by_name("password")
        mypassword = os.environ.get('YOUTUBE_PASSWORD')
        password.send_keys(mypassword)

        # click next button to log in
        pass_next_button = self.browser.find_element_by_id("passwordNext")
        pass_next_button.click()

        sleep(3)

    # add unwatched videos to watchlist
    def add_to_watchlist(self):

        # open show more section
        try:

            more = self.browser.find_elements_by_xpath(
                "//paper-button[@aria-label='Show more']")
            for m in more:

                m.click()
                sleep(3)
        except:

            pass

        # scroll until there are no more videos in the homepage of youtube
        # homepage is around 17-20 scrolls from the bottom of the page
        # tried to check for the loader that appears with every scroll to avoid using the hardcoded value, but the loader does not always appear in decent networks
        i = 0
        while i <= 20:

            try:

                # scroll to the end of the page
                self.browser.find_element_by_tag_name(
                    'body').send_keys(Keys.END)
                act = ActionChains(self.browser)
                act.send_keys(Keys.PAGE_DOWN).perform()

                # allow some time for the videos to get loaded
                sleep(5)

                # proceed to next page with videos
                i = i + 1
            except:

                continue
   
        # set time format
        FMT = '%H:%M:%S'

        # get all video containers
        videos = self.browser.find_elements_by_tag_name(
            "ytd-rich-grid-video-renderer")

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
                    video_company_title = v.find_elements_by_class_name(
                        "yt-simple-endpoint")[2].text

                    # words we dont want to be included in title / company
                    unwanted_text = ['mbcnews', 'mnet k-pop', 'mnet official', 'ytn news', 'jtbc entertainment', 'jtbc drama', 'tvn drama', 'trailer', 'mbcentertainment', 'music bank', 'mcountdown', 'making film', 'vlog', 'asmr', 'clip', 'teaser', 'medley', 'music bank', 'ep.', 'running man', '[hot]', 'behind the scene', 'performance', 'stage', 'practice', 'cam', 'instrumental', 'backstage', 'choreography', 'preview', 'inkigayo', 'dance cover']

                    # check if it contains korean characters and doesnt contain the words:
                    if (any([re.search(u'[\u3131-\ucb4c]', x) for x in video_title]) or any([re.search(u'[\u3131-\ucb4c]', x) for x in video_company_title])) and len([el for el in unwanted_text if el in video_company_title.lower()]) < 1 and  len([el for el in unwanted_text if el in video_title.lower()]) < 1 :

                        # print("TITLE: " + video_title.lower())
                        # print("COMPANY: " + video_company_title.lower())

                        # check if already watched
                        try:

                            v.find_element_by_id('progress')
                            #print("already watched\n")
                            continue
                        except Exception:

                            # hover on element
                            hover = ActionChains(
                                self.browser).move_to_element(v)
                            hover.perform() 

                            # check if already in watchlist
                            try:

                                v.find_element_by_xpath(
                                    "//ytd-thumbnail-overlay-toggle-button-renderer[contains(@aria-label, 'Added')]")
                                #print("already in watchlist\n")
                                continue
                            except Exception:

                                # print("Name korean -" + video_title + " OR " + video_company_title)
                                # print("Time looks ok - " + str(time_vid) + '\n')

                                # hover on element
                                hover = ActionChains(
                                    self.browser).move_to_element(v)
                                hover.perform()

                                try:

                                    # add video in watchlist
                                    v.find_element_by_xpath(
                                        "//ytd-thumbnail-overlay-toggle-button-renderer[contains(@aria-label, 'Watch later')]").click()
                                
                                    # wait before proceeding
                                    sleep(1)
                                except:

                                    continue
                    else:

                        continue
                        #print("no korean\n")
                else:

                    continue
                    #print("wrong time\n")
            except:

                continue


# main
if __name__ == "__main__":

    YoutubeList().__init__()
