from bs4 import BeautifulSoup
import datetime
from utils import aoai_util
import json

# 讀取 activity.html 檔案
with open("src/activity.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# 取得今天的日期
today = datetime.datetime.today().strftime('%Y-%m-%d')
chinese_date = datetime.datetime.today().strftime('%m月%d日')


def format_question():
    with open("src/text/usage_log.json", "r", encoding="utf-8") as file:
        text = file.read()
    lore = """
    你是一個統整內容的專家，你的輸入是一個 JSON 檔案，內容是使用者今日的應用程式使用時間。  
    你的任務是根據應用程式的使用時間，統整出使用者今天的活動內容，並根據統整內容，為其分類 1 到 3 種標籤 (tags)。  

    請將輸出格式設為 JSON，包含以下欄位：
    - "summary": 根據使用時間整理的統整內容。
    - "tags": 一個陣列，內含 1 到 3 個標籤，標籤應代表統整內容的類別，例如：「工作」、「學習」、「娛樂」等。  

    請確保標籤能準確反映統整內容，例如：
    - 若應用程式多為「程式開發工具」，則標籤可能為 ["工作", "學習"]。
    - 若應用程式多為「遊戲與影音」，則標籤可能為 ["娛樂"]。  

    請確保輸出結果符合 JSON 格式，不包含額外的解釋或多餘的文字。  
    """
    question = f"請將以下檔案進行統整：\n{text}"
    return lore, question

def get_summarize():
    lore, question = format_question()
    client = aoai_util.get_client("gpt-4o")
    answer = aoai_util.get_client_answer(client, "gpt-4o", lore, question , 0.1)
    return answer

def main(date):
    global soup, chinese_date
    usage_chart_file = f"img/activity/{date}_usage_log.png"
    
    summarize = get_summarize()
    parsed_summarize = json.loads(summarize)
    tags = parsed_summarize.get("tags", [])
    summarize = parsed_summarize.get("summary", "")
    # 檢查是否已經有當天的紀錄，避免重複插入
    existing_entries = soup.find_all("span", class_="ml-2")
    if any(today in entry.text for entry in existing_entries):
        print(f"已經有 {today} 的紀錄，不重複插入！")
    else:
        # 生成新的活動卡片 HTML
        new_card = soup.new_tag("div", **{"class": "bg-white border rounded-lg overflow-hidden shadow-lg"})
        
        # 生成卡片的圖片部分
        a_tag = soup.new_tag("a", href=f"src/daily/{today}.html")
        img_tag = soup.new_tag("img", src=usage_chart_file, alt="Activity image", **{"class": "w-full h-48 object-cover"})
        a_tag.append(img_tag)
        new_card.append(a_tag)

        content_div = soup.new_tag("div", **{"class": "p-4"})

        info_div = soup.new_tag("div", **{"class": "flex items-center text-gray-500 text-sm mb-2"})
        admin_span = soup.new_tag("span", **{"class": "mr-2"})
        admin_span.string = "Admin"
        dot_span = soup.new_tag("span")
        dot_span.string = "•"
        date_span = soup.new_tag("span", **{"class": "ml-2"})
        date_span.string = today

        info_div.extend([admin_span, dot_span, date_span])
        content_div.append(info_div)

        title_a_tag = soup.new_tag("a", href=f"src/daily/{today}.html")
        title_h3 = soup.new_tag("h3", **{"class": "text-lg font-semibold mb-2"})
        title_h3.string = chinese_date
        title_a_tag.append(title_h3)
        content_div.append(title_a_tag)

        desc_p = soup.new_tag("p", **{"class": "text-gray-700 mb-4"})
        desc_p.string = summarize
        content_div.append(desc_p)

        footer_div = soup.new_tag("div", **{"class": "flex items-center justify-between text-gray-500 text-sm"})

        tags_div = soup.new_tag("div", **{"class": "flex items-center"})
        tag_icon = soup.new_tag("i", **{"class": "fas fa-tags mr-1"})
        tag_span = soup.new_tag("span")
        tag_span.string = " ".join(tags)
        tags_div.extend([tag_icon, tag_span])

        heart_icon = soup.new_tag("i", **{"class": "far fa-heart"})

        footer_div.extend([tags_div, heart_icon])
        content_div.append(footer_div)

        new_card.append(content_div)

        # 找到正確的插入位置（活動記錄的區塊）
        activity_container = soup.find("div", class_="grid grid-cols-1 md:grid-cols-3 gap-8")
        if activity_container:
            activity_container.insert(0, new_card)  # 插入最前面，最新的紀錄顯示在第一個

            # 寫回 activity.html
            with open("src/activity.html", "w", encoding="utf-8") as file:
                file.write(str(soup.prettify()))

            print(f"已成功加入 {today} 的活動紀錄！")
        else:
            print("找不到活動紀錄的區塊，無法插入！")
