from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import Constant as C
import time

app = Flask(__name__)

# options = Options()
# # options.add_argument("--headless")
# driver = webdriver.Firefox(options=options)
# wait = WebDriverWait(driver, 60)
# driver.get('https://hasbercourier.easyenvios.com/')

def SearchFileWeb(suministro):
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 60)
    driver.get('https://hasbercourier.easyenvios.com/')

    sandbox = wait.until(EC.presence_of_element_located((By.ID,C.exp.box)))
    sandbox.send_keys(suministro)

    sendContent = wait.until(EC.presence_of_all_elements_located((By.XPATH,C.exp.btn)))
    sendContent[0].click()

    time.sleep(3)
    Framesubdoc = wait.until(EC.presence_of_element_located((By.ID,C.exp.subdoc))).get_attribute('src')
    driver.quit()

    return Framesubdoc, suministro

@app.route('/search', methods=['POST'])
def search_file():
    data = request.get_json()
    suministro = data.get('suministro')
    if not suministro:
        return jsonify({'error': 'Missing suministro parameter'}), 400

    try:
        result = SearchFileWeb(suministro)
        # return jsonify({'url': result[0], 'suministro': result[1]})
        return jsonify({'url': result[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)
