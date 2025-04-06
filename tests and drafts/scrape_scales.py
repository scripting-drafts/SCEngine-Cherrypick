# https://plucknplay.github.io/en/scale-list.html
import csv
from os import path
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import enhancements.turquoise_logger as turquoise_logger
import enhancements.mod_initializer as gui_enhancements
import colorama
from sys import exit

class SeleniumWireModule:
    def __init__(self):
        colorama.init()
        GREEN = colorama.Fore.GREEN
        GRAY = colorama.Fore.LIGHTBLACK_EX
        RESET = colorama.Fore.RESET
        RED = colorama.Fore.RED

        gui_enhancements.run_sel()
        logg = turquoise_logger.Logger()
        path_firefox_binary = 'resources/geckodriver.exe'
        path_geckodriver_log = path.abspath('resources/geckodriver.log')
        log = logg.logging()
        localhost = '127.0.0.1'
        initial_url = 'https://www.google.com'
        target_url = 'https://plucknplay.github.io/en/scale-list.html'

        options = Options()
        options.add_argument('--headless')
        options.set_preference('dom.webnotifications.enabled', False)
        options.set_preference('dom.push.enabled', False)
        options.set_preference('dom.webdriver.enabled', False)
        options.set_preference('useAutomationExtension', False)
        options.set_preference('privacy.trackingprotection.enabled', True)

        options.set_preference('browser.cache.disk.enable', False)
        options.set_preference('browser.cache.memory.enable', False)
        options.set_preference('browser.cache.offline.enable', False)
        options.set_preference('network.http.use-cache', False)

        # USER AGENT OPT
        # options.set_preference('intl.accept_languages', random.choice(localesList).lower())
        # options.set_preference('general.useragent.override', random.choice(userAgentList))

        profile_path = open('resources/profile_path', 'r').read()

        driver = webdriver.Firefox(firefox_profile=profile_path,
                                   options=options, executable_path=path_firefox_binary,
                                   service_log_path=path_geckodriver_log)
        driver.implicitly_wait(10)
        log.debug(f'Webdriver is UP')

        self.log = log
        self.localhost = localhost
        self.initial_url = initial_url
        self.target_url = target_url
        self.driver = driver

    def healthcheck(self):
        '''1 Returns an int if dead and None if alive  
        2 Throws a WebDriverException if dead'''
        self.log.debug('Webdriver healthcheck going on')
        try:
            assert(self.driver.service.process.poll() == None)
            self.driver.service.assert_process_still_running()
            self.log.debug('The driver appears to be OK')
            status = True
        except Exception as e:
            self.log.debug(f'The driver appears to be NOK - {e}')
            status = False
        
        return status

    def connection_attempt(self, url=None, max_attempts_count=2):
        '''Commits attempts_count connection attempts to the given initial_url'''
        attempts_count = 1

        while not attempts_count > max_attempts_count:
            self.log.debug(f'{self.localhost} <-> {url}')
            self.driver.get(url)

            if len(self.driver.requests) > 0:
                if self.driver.requests[0].response.status_code == 200:
                    self.log.debug(f''''Connection reached | Attempts: {attempts_count}
                                        
            Functioning server will proceed to target
                                   
                                    ''')
                    attempts_count = max_attempts_count
                    is_connected = True
            
            else:
                self.log.debug(f'Failed to connect | Attempts: {attempts_count}')
                is_connected = False

            attempts_count += 1
            
        self.is_connected = is_connected

    def requests_vars_get(self):
        '''Outputs REQ (Request URL), STAT (Status Code) and CT (Content Type) within responses in requests'''
        print('\n' + 'Responses summary')
        log = self.log
        if self.is_connected:
            for request in self.driver.requests:
                if request.response:
                    log.debug(f'REQ: {request.url}')
                    log.debug(f'STAT: {request.response.status_code}')
                    log.debug('CT:' +  request.response.headers['content-type'] + '\n')
                    self.req_stat_ct = [str(request.url), str(request.response.status_code), request.response.headers['content-type']]

                del self.driver.requests
        if not self.is_connected:
            log.debug('The driver is not available')

    def tearDown(self):
        log = self.log
        log.debug('''
                  
            Graceful shutdown and status verification
                  
                  ''')
        
        self.driver.quit()
        log.debug('Verifying webdriver shutdown')
        status = self.healthcheck()

        if status == False:
            log.debug('Successful driver termination')
        else:
            log.error('Unsuccessful driver termination')

    def scrape_info(self):
        '''Ecclesiastical Modes'''
        log = self.log
        self.connection_attempt(url=self.target_url, max_attempts_count=1)
        self.requests_vars_get()

        Scale_Names = self.driver.find_element(By.CSS_SELECTOR, 'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > b:nth-child(1)').text
        'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)'

        scale_dict = {}
        datalist = []
        musical_modes = 3 # 1st Mode in page
        try:
            data = {}
            Title, Name, Intervals, AKA = 'Title' + ''.join([self.driver.find_element(By.CSS_SELECTOR, 'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > th:nth-child({})'.format(str(x))).text for x in [2, 3, 4]])
            log.debug(f'{Title}, {Name}, {Intervals}, {AKA}')
        
            Scale_Names_Amount = 0

            for i in range (90):
                self.driver.find_element(By.CSS_SELECTOR, f'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child({i}) > td:nth-child(1) > b:nth-child(1)')

            scales_name = self.driver.find_element(By.CSS_SELECTOR, 'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > b:nth-child(1)').text
            
            for i in range(2, 4):
                data['Scale Name'], data['Name'], data['Intervals'], data['AKA'] = self.driver.find_element(By.CSS_SELECTOR, f'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child({i})')
            'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)'

            for musical_mode_position in range(3, 40):
                data = {}
                # titles_count = 0
                # try:
                #     title = self.driver.find_element(By.CSS_SELECTOR, f'#page > section:nth-child(3) > h2:nth-child({position})')
                #     data['title'] = title.text

                #     tr = f'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child({})'    # 7
        
                # except Exception as e:
                #     log.debug('Warning: No Title Exception')
                #     log.debug(f'Exception: {e}')

        except Exception as e:
            log.debug('Warning: No Title Exception')
            log.debug(f'Exception: {e}')

    #         for line in column_lines:
                
    #             tr = f'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child({})'    # 7

        
    #             for musical_mode_position in range(3, 40):
    #                 data = {}
    #                 titles_count = 0
    #                 try:
    #                     title = self.driver.find_element(By.CSS_SELECTOR, f'#page > section:nth-child(3) > h2:nth-child({position})')
    #                     data['title'] = title.text

    #                     tr = f'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child({})'    # 7


                

    #                 except Exception as e:
    #                     log.debug('Warning: No Title Exception')
    #                     log.debug(f'Exception: {e}')
                
    #         for position in 999999:
    #                     contents_selector = 'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(7)'

        
    #     # get all h2's titles
    #     #page > section:nth-child(3) > h2:nth-child(3)'
    #     # other h2 title
    #     #page > section:nth-child(3) > h2:nth-child(5)
    #     # get all tr's
    #     #table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(7)
    #     for position in 999999:
    #         try:
    #             tr = 'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(7)'
    #             scale_list['generic_names'] = self.driver.find_element_by_css_selector('table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > b:nth-child({})'.format(position))
    #             # get all scale_names easy

    #             for name in 
    #             try:

    #         except Exception as e:
    #             print(e)

    #     return
    
    # def write_to_csv(datalist):
    #     keys = datalist[0].keys()

    #     with open('./scales.csv', 'w', encoding='utf_8_sig', newline='') as f:
    #         dict_writer = csv.DictWriter(f, keys, dialect='excel', delimiter=';')
    #         dict_writer.writeheader()
    #         dict_writer.writerows(datalist)

# TEST
wm = SeleniumWireModule()
wm_is_up = wm.healthcheck()

if wm_is_up:
    is_connected = wm.connection_attempt(wm.initial_url)
    wm.requests_vars_get()

wm.scrape_info()
wm.tearDown()

# parent
'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)'
# generic_names
'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > b:nth-child(1)'
# scales_names
'table.lists:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)'