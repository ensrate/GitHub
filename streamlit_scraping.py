from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import streamlit as st

def scrape_reviews(url):
    # Chrome 웹 드라이버 설정
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    wait = WebDriverWait(driver, 10)

    # URL로 이동
    driver.get(url)

    rate_path = './div[1]/a/div/div[1]/div[1]/span'
    review_path = './div[1]/a/div/p'

    rate_list = []
    review_list = []

    prod_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'item_rvw_list')))
    lis = prod_list.find_elements(By.TAG_NAME, 'li')

    for li in lis:
        review = li.find_element(By.XPATH, review_path).text
        review_list.append(review)

        rate = li.find_element(By.XPATH, rate_path).text
        rate_list.append(rate)

    for page in range(2, 62):
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//a[@onclick=\"fn_GoCommentPage('{page}')\"]")))
        element.click()

        prod_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'item_rvw_list')))
        lis = prod_list.find_elements(By.TAG_NAME, 'li')

        for li in lis:
            review = li.find_element(By.XPATH, review_path).text
            review_list.append(review)

            rate = li.find_element(By.XPATH, rate_path).text
            rate_list.append(rate)

    driver.quit()

    review_data = {
        '리뷰': review_list,
        '평점': rate_list,
    }

    review_df = pd.DataFrame(review_data)
    review_df['평점'] = review_df['평점'].astype(int)

    return review_df

def main():
    st.title("아디다스 운동화 리뷰 스크래핑 및 분석")
    
    # 사용자로부터 제품 URL 입력
    url = st.text_input("아디다스 운동화 제품의 리뷰를 스크래핑할 URL을 입력하세요:")
    
    if st.button("리뷰 스크래핑 시작") and url:
        st.text("리뷰 스크래핑 중...")
        review_df = scrape_reviews(url)
        st.text("리뷰 스크래핑 완료!")

        # 스크래핑한 데이터 출력
        st.write("스크래핑한 리뷰 데이터:")
        st.write(review_df)

        # 긍정적인 리뷰와 부정적인 리뷰로 분류
        label_list = ['긍정' if i >= 4 else '부정' for i in review_df['평점']]
        review_df['분류'] = label_list

        # 분류한 데이터 출력
        st.write("긍정적인 리뷰 및 부정적인 리뷰:")
        st.write(review_df[['리뷰', '분류']])
