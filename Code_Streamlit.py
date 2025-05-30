
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
import plotly.express as px


# 필요 라이브러리 import
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Selenium으로 웹 드라이버를 실행

@st.cache_data
def load__df(url1,url2):

    driver = webdriver.Chrome()

    # ------ JobKorea------

    driver.get(url1)
    time.sleep(3)

    # 크롤링 및 df 저장
    divs = driver.find_elements(By.CSS_SELECTOR , 'div[class^="Flex_display_flex__i0l0hl2 Flex_gap_space24__i0l0hlp styles_py_space28__dk46ts8f styles_px_space20__dk46ts2k"]')
    time.sleep(2)

    site_list = []
    company_list = []
    recruit_list = []
    details = []
    details_list = []
    link_list = []

    for div in divs:
        details = []
        site = 'Job_Korea'
        company = div.find_element(By.CSS_SELECTOR, 'span[class*="Typography_variant_size16__344nw26 Typography_weight_regular__344nw2d Typography_color_gray900__344nw2k styles_mr_space4__dk46ts22"]').text
        recruit = div.find_element(By.CSS_SELECTOR, 'span[class*="Typography_variant_size18__344nw25 Typography_weight_medium__344nw2c Typography_color_gray900__344nw2k Typography_truncate__344nw2t"]').text
        detail_block = div.find_elements(By.CSS_SELECTOR, 'div[class*="Flex_direction_row"]')
        for detail_div in detail_block:
            spans = detail_div.find_elements(By.TAG_NAME, 'span')
            for span in spans:
                details.append(span.text) 
        link = div.find_element(By.CSS_SELECTOR, 'a[href*="/Recruit/GI_Read/"]').get_attribute("href")
        
        site_list.append(site)
        company_list.append(company)
        recruit_list.append(recruit)
        details_list.append(details)
        link_list.append(link)

    data1 = {'Site':site_list, 'Col_Company':company_list, 'Col_Recruit':recruit_list, 'Col_detail':details_list, 'Col_url':link_list}
    df_jobkorea = pd.DataFrame(data1)

    # ------ Saramin------

    driver.get(url2)
    time.sleep(3)

    # 크롤링 및 df 저장
    divs = driver.find_elements(By.CSS_SELECTOR , 'div[class^="item_recruit"]')
    time.sleep(2)

    site_list = []
    company_list = []
    recruit_list = []
    details = []
    details_list = []
    link_list = []

    for div in divs:
        details = []
        site = 'Saramin'
        company = div.find_element(By.CSS_SELECTOR, 'a[class*="track_event data_layer"]').text
        recruit = div.find_element(By.CSS_SELECTOR, 'h2.job_tit a span').text
        span_block = div.find_elements(By.CSS_SELECTOR, 'div.job_condition span')
        for span in span_block:
            details.append(span.text) 
        link = div.find_element(By.CSS_SELECTOR, 'h2.job_tit a').get_attribute("href")
        
        site_list.append(site)
        company_list.append(company)
        recruit_list.append(recruit)
        details_list.append(details)
        link_list.append(link)

    data2 = {'Site':site_list, 'Col_Company':company_list, 'Col_Recruit':recruit_list, 'Col_detail':details_list, 'Col_url':link_list}
    df_saramin = pd.DataFrame(data2)

    df = pd.concat([df_jobkorea, df_saramin]).reset_index(drop=True)
    driver.quit()
    
    return df

def prep_df(df):
    df_prep = df.groupby('Site').size().reset_index(name='Count')
    df_prep['Ratio'] = round(df_prep['Count']/ df_prep['Count'].sum()*100, 2)
    
    return df_prep

if __name__ == "__main__":

  st.title('Title')
  # URL
  url1 = 'https://www.jobkorea.co.kr/Search/?stext=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D'
  url2 = url = 'https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D'
  
  
with st.form('form', clear_on_submit = True):
  submitted1 = st.form_submit_button('RecruitSearching')
  if submitted1:
    df = load__df(url1,url2)
    df_prep = prep_df(df)
    fig = px.pie(df_prep, names='Site', values='Count')

    st.dataframe(df)
    st.dataframe(df_prep)
    st.subheader("Recruitment Ratio")
    st.plotly_chart(fig, use_container_width=True)
