from selenium import webdriver
import argparse
from time import sleep

def main():
    parser = argparse.ArgumentParser(description='Login to Titech Portal')
    parser.add_argument('account', metavar='ACCOUNT', type=str, help='account name to login')
    parser.add_argument('password', metavar='PASSWORD', type=str, help='password to login')
    parser.add_argument('passcode', metavar='PASSCODE', type=str, help='the file path which contains the passcode')
    parser.add_argument('--browser', '-e', default='chrome',
            choices=['chrome', 'safari', 'firefox', 'ie', 'edge'],
            help="browser to open the web page, default is set to Chrome, available broswer are:\n"
                    "(1) Google-Chrome   \n"
                    "(2) Safari          \n"
                    "(3) Mozilla Firefox \n"
                    "(4) Internet Explorer \n"
                    "(5) Microsoft Edge.")

    args = parser.parse_args()

    code = getCode(args.passcode)

    # Start the browser
    driver = None
    if args.browser == 'safari':
        driver = webdriver.Safari(keep_alive=True)
    elif args.browser == 'chrome':
        driver = webdriver.Chrome()
    elif args.browser == 'firefox':
        driver = webdriver.Firefox()
    elif args.browser == 'ie':
        driver = webdriver.Ie()
    elif args.browser == 'edge':
        driver = webdriver.Edge()
    else:
        print("Unavailable browser, please check --browser parameter")
        exit()


    driver.get("https://portal.nap.gsic.titech.ac.jp/GetAccess/Login?Template=userpass_key&AUTHMETHOD=UserPassword")


    # input user name
    element = driver.find_element_by_name("usr_name")
    element.clear()
    element.send_keys(args.account)

    # input password
    element = driver.find_element_by_name("usr_password")
    element.clear()
    element.send_keys(args.password)

    # submit format
    element = driver.find_element_by_name("OK")
    element.click()

    sleep(5)

    # passcode input page
    elements = driver.find_elements_by_tag_name("th")

    i = 0
    for e in elements:
        if len(e.text) > 0:
            element = driver.find_element_by_name("message" + str(3 + i))
#            element = webdriver.support.ui.WebDriverWait(driver, 3).until(lambda x: x.find_element_by_name("message" + str(3 + i)))
            element.clear()
            element.send_keys(code[e.text])
            i = i + 1

    element = driver.find_element_by_name("OK")
    element.click()

    sleep(10)
    driver.close()

def getCode(path):
    code = dict()

    f = open(path, "r")
    passcode = f.readlines()
    passcode = [p.split() for p in passcode]

    for c in range(ord('A'), ord('K')):
        for n in range(1, 8):
            key = ("[%s,%s]") % (chr(c), str(n))
            code[key] = passcode[n - 1][c - ord('A')]

    return code

if __name__ == '__main__':
    main()
