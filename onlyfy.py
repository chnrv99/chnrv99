import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
import json
import pyperclip
import os

# https://www.zoho.com/recruit/developer-guide/apiv2/

# igonore the certificate errors
edge_options = webdriver.EdgeOptions()
edge_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Edge(options=edge_options)

def getTableContents(table):
    contents = ''
    t_rows = table.find_elements(By.TAG_NAME, 'tr')

    for i in range(len(t_rows)):
        row = t_rows[i].find_elements(By.TAG_NAME, 'td')
        for cell in row:
            print(cell.text.replace("\n", " "), end=' | ')
            contents += cell.text.replace("\n", " ") + ' | '
        print()
        contents += '\n'
    return contents

def getTitleAndDescription(article):
    h2 = article.find_element(By.TAG_NAME, 'h2')
    p = article.find_element(By.TAG_NAME, 'p')
    
    print(h2.text)
    print(p.text)
    contents = h2.text + '\n' + p.text + '\n'
    return contents

def getH5(h5):
    print(h5.text)
    return h5.text

def click_all_buttons(buttons_to_click, clicked_buttons, article):
    for button_to_click in buttons_to_click:
        if button_to_click in clicked_buttons:
            continue
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_to_click)
        time.sleep(0.5)
        arrow_button = button_to_click.find_element(By.TAG_NAME, 'svg')
        arrow_button.click()
        print("Arrow button clicked")
        
        # Add the button to the set of clicked buttons
        clicked_buttons.add(button_to_click)
        
        # Find new buttons that appear after clicking using the article element
        new_buttons =  article.find_elements(By.CSS_SELECTOR, '.sc-hBURRC.sc-fFehDp.sc-clIAKW.bhpqyO.ffwWXK.ciuLQT') 
        new_buttons = [btn for btn in new_buttons if btn not in clicked_buttons]
        time.sleep(0.5)
        
        if new_buttons:
            click_all_buttons(new_buttons, clicked_buttons, article)

  
def getResponseAndRequestSample(element):
    
    ul = element.find_element(By.CLASS_NAME, 'react-tabs__tab-list')
    lis = ul.find_elements(By.TAG_NAME, 'li')
    response = ''
    for li in lis:
        # if the li's attribute aria-selected is false, then click on it
        if li.get_attribute('aria-selected') == 'false' and li.text not in ["Python", "Node.js", "Curl", "Java", "C#"]:
            li.click()
            time.sleep(0.5)
            # use the copy button to copy the response
            copy = element.find_element(By.CLASS_NAME, 'sc-khQdMy')
            copy.click()
            json_str = pyperclip.paste()
            try:
                minimized_json_str = json_str
                # Convert the JSON string to a Python dictionary
                data = json.loads(json_str)
                # Convert the dictionary back to a JSON string, minimized without unnecessary whitespace
                minimized_json_str = json.dumps(data, separators=(',', ':'))
            except json.JSONDecodeError:
                minimized_json_str = json_str

            print(li.text + "\n" + minimized_json_str + "\n")
            response += li.text + "\n" + minimized_json_str + "\n"
            time.sleep(0.5)
        elif li.text not in ["Python", "Node.js", "Curl", "Java", "C#"]:
            # the li's attribute aria-selected is true, so just copy the response
            copy = element.find_element(By.CLASS_NAME, 'sc-khQdMy')
            time.sleep(0.5)
            copy.click()
            # get the text by pyperclip
            # response += li.text + ":\n" + pyperclip.paste() + '\n'
            json_str = pyperclip.paste()

            try:
                minimized_json_str = json_str
                # Convert the JSON string to a Python dictionary
                data = json.loads(json_str)
                # Convert the dictionary back to a JSON string, minimized without unnecessary whitespace
                minimized_json_str = json.dumps(data, separators=(',', ':'))
            except json.JSONDecodeError:
                minimized_json_str = json_str
            
            print(li.text + "\n" + minimized_json_str + "\n")
            response += li.text + "\n" + minimized_json_str + "\n"
            time.sleep(0.5)
    return response
            
      
filenames = []

def getContentsGuide(id):
    filename = id.split('/')[-2] + " " +  '_' + id.split('/')[-1]
    filename = filename.replace('.', ' ')
    filename = filename.replace('_', ' ')
    filename = filename.replace('-', ' ')
    filename = filename.replace('(', ' ')
    filename = filename.replace(')', ' ')
    filename = filename.replace('~', ' ').replace("{", " ").replace("}", " ")
    filename = re.sub(r'\d+', '', filename)
    
    filename = filename.title()
    filename = filename.replace(" ", '')
    filename = filename[0].lower() + filename[1:]
    # input("Filename: "+ filename)
    api_filename = 'onlyfy_api_'
    guide_filename = 'onlyfy_guide_'
    webhook_filename = 'onlyfy_webhook_'
    article = driver.find_element(By.ID, id)
    
    contents = article.text + '\n'
    # write the contents to a file
    choice = '2'
    if choice == '1':
        if filename not in filenames:
            with open(api_filename + filename + '.txt', 'w', encoding='utf8') as file:
                file.write(contents)
            with open('metadata.txt', 'a', encoding='utf8') as file:
                file.write(api_filename + filename + ', ' + id + '\n')
            filenames.append(filename)
        else:
            filename = filename + random.randint(1, 5)
            with open(api_filename + filename + '.txt', 'w', encoding='utf8') as file:
                file.write(contents)
            with open('metadata.txt', 'a', encoding='utf8') as file:
                file.write(api_filename + filename + ', ' + id + '\n')
            filenames.append(filename)
    elif choice == '2':
        with open(guide_filename + filename + '.txt', 'w', encoding='utf8') as file:
            file.write(contents)
    elif choice == '3':
        with open(webhook_filename + filename + '.txt', 'w', encoding='utf8') as file:
            file.write(contents)
    else:
        print("Invalid choice")
    

def getContents(id, choice):
    # input("ID: " + id)
    filename = id.split('/')[-2] + " " +  '_' + id.split('/')[-1]
    filename = filename.replace('.', ' ')
    filename = filename.replace('_', ' ')
    filename = filename.replace('-', ' ')
    filename = filename.replace('(', ' ')
    filename = filename.replace(')', ' ')
    filename = filename.replace('~', ' ').replace("{", " ").replace("}", " ")
    filename = re.sub(r'\d+', '', filename)
    
    filename = filename.title()
    filename = filename.replace(" ", '')
    filename = filename[0].lower() + filename[1:]
    # input("Filename: "+ filename)
    api_filename = 'onlyfy_api_'
    guide_filename = 'onlyfy_guide_'
    webhook_filename = 'onlyfy_webhook_'
    article = driver.find_element(By.ID, id)
    # find all child elements of article
    child_elements = article.find_elements(By.XPATH, './/*')
    
    # first click all buttons with classname sc-eDZJfc
    buttons = article.find_elements(By.CLASS_NAME, 'jekxwK') #200
    buttons = buttons + article.find_elements(By.CLASS_NAME, 'epQWfk') #400
    # input("length of response buttons: " + str(len(buttons)))
    for button in buttons:
        button.click()
        # input("response Button clicked")
        time.sleep(1)
        
    
    ###
    buttons_to_click = article.find_elements(By.CSS_SELECTOR, '.sc-hBURRC.sc-fFehDp.sc-clIAKW.bhpqyO.ffwWXK.ciuLQT')
    # input("length of buttons to click: " + str(len(buttons_to_click)))  
    print("Initial length of buttons to click: " + str(len(buttons_to_click)))
    # Start clicking all buttons
    click_all_buttons(buttons_to_click,set(), article)
    ###
    
    # input("Press Enter to continue, all buttons clicked")

    contents = ''
    try:
        contents += getTitleAndDescription(article)
    except NoSuchElementException:
        print("Element not found")
        
        
    button = article.find_element(By.CLASS_NAME, 'sc-jHkVfK')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    button.click()
    time.sleep(1.5)
    # input("URL Button clicked")
    req_method = button.find_element(By.CLASS_NAME, 'sc-bQtJOP')
    # input("Request method: " + req_method.text)
    contents += "Request method: " + req_method.text + '\n'
    buttoon = article.find_element(By.CLASS_NAME, 'sc-jWUzTF')
    # input("url:" + buttoon.text)
    request_url = buttoon.text   
    contents += "Endpoint:" + buttoon.text + '\n\n'
    button.click()
    
    for element in child_elements:
        # try:
            if element.tag_name == 'h5':
                contents += getH5(element)  + '\n'
            if element.tag_name == 'table' and 'RESPONSE' not in element.text:
                contents += getTableContents(element) 
            if element.tag_name == 'h3':
                if element.text == 'Responses' or element.text == 'Request samples' or element.text == 'Response samples':
                    break
                print(element.text)
                contents += element.text + '\n'
            if element.get_attribute('class') == 'sc-fIoroj etIVBB':
                print(element.text)
                contents += element.text + '\n'
            # if element.tag_name == 'div' and element.get_attribute('class') == 'sc-cabOPr':
                # contents += getResponseAndRequestSample(element)
        # except NoSuchElementException:
            # print("Element not found")
    
    # find all divs with classname sc-fmZqYP which has the responses and schema
    divs = article.find_elements(By.CLASS_NAME, 'sc-fmBDoT')
    count = 0
    print("Responses")
    contents += "\n\nResponses:\n"
    buttons = article.find_elements(By.CLASS_NAME, 'sc-eFehXo')
    for div in divs:
        print(buttons[count].text)
        contents += buttons[count].text + '\n'
        count += 1
        child_elements = div.find_elements(By.XPATH, './/*')
        for element in child_elements:
            if element.tag_name == 'h5':
                contents += getH5(element) + '\n'  
            if element.tag_name == 'table':
                contents += getTableContents(element) 
                
    # url of api is in this button with class sc-jGNhvO
    # try:
        # button = article.find_element(By.CLASS_NAME, 'sc-iEXKAA')
        # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        # button.click()
        # time.sleep(1.5)
        # # input("URL Button clicked")
        # req_method = button.find_element(By.CLASS_NAME, 'sc-EgOXT')
        # input("Request method: " + req_method.text)
        # contents += "Request method: " + req_method.text + '\n'
        # buttoon = article.find_element(By.CLASS_NAME, 'sc-hHOBiw')
        # input("url:" + buttoon.text)
        # request_url = buttoon.text   
        # contents += "Endpoint:" + buttoon.text + '\n\n'
        # button.click()
        
    # find all h3 tags with classname sc-kDvujY
    h3s = article.find_elements(By.CLASS_NAME, 'sc-kDThTU')
    #find all div tags with classname sc-cabOPr
    divs = article.find_elements(By.CLASS_NAME, 'sc-caiKgP')
    
    for h3, div in zip(h3s, divs):
        print(h3.text)
        contents += h3.text + '\n'
        contents += getResponseAndRequestSample(div) + '\n'
    # except NoSuchElementException:
    #     print("Element not found")
        try:
            buttons = article.find_elements(By.CLASS_NAME, 'sc-eFehXo')
            for button in buttons:
                print(button.text)
                contents += button.text + '\n'
            h3s = article.find_elements(By.CLASS_NAME, 'sc-kDThTU')
            #find all div tags with classname sc-cabOPr
            divs = article.find_elements(By.CLASS_NAME, 'sc-caiKgP')
            for h3, div in zip(h3s, divs):
                print(h3.text)
                contents += h3.text + '\n'
                contents += getResponseAndRequestSample(div) + '\n'
        except NoSuchElementException:
            print("Element not found")
            
    
    # write the contents to a file
    # choice = '1'
    # filename = input('Enter filename: ')
    request_url = request_url.replace('\n', ' ')
    try:
        contents = """***metaDataStart
{
    "Method" : """ + req_method.text + """,
    "API Endpoint" : """ + request_url + """,
}
metaDataEnd***""" + '\n\n' + contents
    except:
        pass
    if choice == '1':
        if filename not in filenames:
            with open(api_filename + filename + '.txt', 'w', encoding='utf8') as file:
                file.write(contents)
            with open('metadata.txt', 'a', encoding='utf8') as file:
                file.write(api_filename + filename + ', ' + id + '\n')
            filenames.append(filename)
        else:
            filename = filename + random.randint(1, 5)
            with open(api_filename + filename + '.txt', 'w', encoding='utf8') as file:
                file.write(contents)
            with open('metadata.txt', 'a', encoding='utf8') as file:
                file.write(api_filename + filename + ', ' + id + '\n')
            filenames.append(filename)
    elif choice == '2':
        with open(guide_filename + filename + '.txt', 'w', encoding='utf8') as file:
            file.write(contents)
    elif choice == '3':
        with open(webhook_filename + filename + '.txt', 'w', encoding='utf8') as file:
            file.write(contents)
    else:
        print("Invalid choice")
    
    
    # print("Final contents: \n\n", contents)

# base url
url = 'https://onlyfy.io/doc/v1#operation/StatusSetGet'
driver.get(url)
time.sleep(2)



# need to get all a tags under ul and li
# get all data-item-id attributes in li and print them
ul = driver.find_element(By.CLASS_NAME, 'scrollbar-container')
li_elements = ul.find_elements(By.TAG_NAME, 'li')
div_ids = []
count = 0
duplicates = 0
for li in li_elements:
    print(li.get_attribute('data-item-id'))
    if li.get_attribute('data-item-id') in div_ids:
        duplicates += 1
    else:
        div_ids.append(li.get_attribute('data-item-id'))
        count += 1
print("Total count: ", count)
print("Duplicates: ", duplicates)
   
result = {} 
for entry in div_ids:
    parts = entry.split('/')
    folder = '/'.join(parts[:-1])  # Get the folder name by excluding the last part
    if folder not in result:
        result[folder] = []
    if 'operation' in parts:
        result[folder].append(entry)

# Remove folders without operations (empty lists)
result = {k: v for k, v in result.items() if v}

# getContents('operation/offboarding.completed')

# iterate thro all div ids

count = 0
input("Total div ids: " + str(len(div_ids)) + ". Press Enter to continue")
input("Length of result: " + str(len(result)))  
for value in div_ids:
    if count >= 0:
        # input("Value: " + value + " Count: " + str(count))
        if 'section' in value:
            getContentsGuide(value)
        elif 'operation' in value:
            getContents(value, '1')
    count += 1
    

driver.quit()