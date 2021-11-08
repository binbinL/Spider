import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def ProcessSpider():
    # 滚动页面
    js = "return action=document.body.scrollHeight"
    new_height = driver.execute_script(js)  # 获取页面的高度
    # 滚动到页面长度0.7的位置，以50为间隔做滚动,一是为了加载图像，二是为了能够实现点击下一页
    for i in range(0, int(new_height * 0.7), 50):
        driver.execute_script('window.scrollTo(0, %s)' % (i))

    # 用Xpath寻找信息
    title = driver.find_elements(By.XPATH, '//*[@id="component_59"]/li/a')  # 找商品名称信息
    price = driver.find_elements(By.XPATH, '//*[@id="component_59"]/li/p[@class="price"]')  # 商品价格
    imgs = driver.find_elements(By.XPATH, '//*[@id="component_59"]/li/a/img')  # 商品的图片地址
    for t, p, img in zip(title, price, imgs):
        # 把商品信息添加到对应列表中
        titles.append(t.get_attribute("title"))
        prices.append(p.text)
        imgs_url.append(img.get_attribute("src"))


# 翻页
def PageTurn():
    # 把翻页操作放在try里面，防止出现到最后一页无法爬取而导致报错
    try:
        # 用Xpath找到并点击翻页按钮
        page_next = driver.find_element(By.XPATH, '//*[@id="12810"]/div[7]/div[2]/div/ul/li[10]')
        page_next.click()
    except:
        print("当前页面已是最后一页")


def InsertDB():
    try:
        # 存入数据库
        conn = pymysql.connect(host="localhost", user="root", password="root", database="task",
                               charset='utf8')  # 连接数据库
        cs1 = conn.cursor()  # 建立游标
        # 表创建 格式定义
        sqlcreat = '''
             create table if not exists dangdang(
                    title char(100) not null,
                    price char(20) not null,
                    urls char(100) not null
                    )
           '''
        cs1.execute(sqlcreat)
        sql = '''INSERT INTO dangdang(title,price,urls) VALUES("%s","%s","%s")'''

        for i in range(len(titles)):
            # 设置存入信息的数量 学号为031904113 爬取113张
            if i >= 113:
                return
            arg = (titles[i], prices[i], imgs_url[i])  # 设置存入信息
            cs1.execute(sql, arg)
            conn.commit()
    except Exception as err:
        print(err)


def DownLoadImg():
    for i in range(len(imgs_url)):
        # 设置存入信息的数量 学号为031904113 爬取113张
        if i >= 113:
            return
        resp = requests.get(imgs_url[i])  # 通过requests.get()直接访问图像地址
        f = open('./imgs/' + titles[i] + '.jpg', 'wb')  # 二进制保存
        f.write(resp.content)  # 写入
        f.close()  # 关闭


if __name__ == '__main__':
    url = 'http://book.dangdang.com/'  # 当当网
    driver = webdriver.Chrome()  # 创建浏览器对象
    driver.get(url)
    search_content = driver.find_element(By.XPATH, '//*[@id="key_S"]')  # 寻找搜索框
    search_content.send_keys("书包")  # 传入信息：书包
    search_button = driver.find_element(By.XPATH, '//*[@id="form_search_new"]/input[10]')  # 寻找搜索按钮
    search_button.click()  # 点击搜索

    titles = []
    prices = []
    imgs_url = []

    for i in range(2):
        # 爬取两页
        ProcessSpider()
        PageTurn()

    InsertDB()#保存到数据库
    DownLoadImg()#下载图片
    driver.close()  # 关闭
