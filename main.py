from flask import Flask, render_template, request, redirect, url_for, session
import os
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_buddhism_quiz_v2'

# --- 題目資料 ---
questions = [
    {
        "id": 1,
        "image": "q1.jpg",
        "question": "幹部會議的時候，大家在討論卡傳要怎麼規劃，結果行政組組長和副社長就吵起來了...行政組說他都有做，但副社長說行政組都沒做事，兩方互相指責.....我有點手足無措，但是好像要做點什麼...應該怎麼做呢？",
        "options": [
            {"text": "千錯萬錯都是我的錯，沒有居中協調導致誤會。", "scores": {"悲": 1, "智": 1, "力": 1}},
            {"text": "我們看看還要做什麼就接著討論就好。", "scores": {"悲": 0, "智": 2, "力": 1}},
            {"text": "先冷靜現場，後續再分別關心發生了什麼事？", "scores": {"悲": 2, "智": 0, "力": 1}}
        ]
    },
    {
        "id": 2,
        "image": "q2.jpg",
        "question": "期中考的歐趴糖還剩下7包，都是不同系的新生沒有來領的...，老師把那七包全部給我，要我發給這些新生，透過這些歐趴糖關懷新生，可是我都不熟，其他幹部又都在忙考試！怎麼辦？",
        "options": [
            {"text": "哎呀跟新朋友的變熟的機會來了，剛好先加個line方便聯繫", "scores": {"悲": 2, "智": 0, "力": 1}},
            {"text": "啟動時間管理大師屬性，google maps規劃最短路徑，高效送達！", "scores": {"悲": 0, "智": 2, "力": 1}},
            {"text": "有點社恐...但先從第一個人開始吧，或許開始之後發現沒那麼困難呢~",
             "scores": {"悲": 1, "智": 0, "力": 2}}
        ]
    },
    {
        "id": 3,
        "image": "q3.jpg",
        "question": "再兩週，社課就快到了，現在只有幹部報名，可是我們好不容易請到外聘的講師，內容又那麼精彩，怎樣才能邀請到更多同學來參加社課呢？",
        "options": [
            {"text": "不想太目的性的邀約，先約他們吃吃飯再開口", "scores": {"悲": 2, "智": 0, "力": 1}},
            {"text": "跟幹部一起討論宣傳策略，看看還有什麼管道可以讓演講訊息擴散出去！",
             "scores": {"悲": 0, "智": 2, "力": 1}},
            {"text": "沒關係，我找系上同學來情義相挺！", "scores": {"悲": 0, "智": 0, "力": 3}}
        ]
    },
    {
        "id": 4,
        "image": "q4.jpg",
        "question": "我是社團活動的總召，籌備待辦事項已經來到第20條了！老師說，千萬不要一個人做，要用團隊的力量！我要如何請求大家的協助一起完成呢？",
        "options": [
            {"text": "先找很擅長揪朋友一起的老師或同學，觀察他是怎麼做的，自己試著練習看看",
             "scores": {"悲": 0, "智": 2, "力": 1}},
            {"text": "分析現有的待辦事項，部分請各小組承擔，「務必」讓活動順利推進", "scores": {"悲": 0, "智": 1, "力": 2}},
            {"text": "關心幹部們的近況，理解他們對於活動的想法，依據每個人的長處或偏好來分配或讓他們認領事項",
             "scores": {"悲": 2, "智": 0, "力": 1}}
        ]
    },
    {
        "id": 5,
        "image": "q5.jpg",
        "question": "最近快炸了，期中考都還沒讀、還要辦卡傳、又有大專營宣傳，真的快不行了！我知道這些承擔都是學習的一部分，但眼前完全沒有頭緒，不知道怎麼辦.....",
        "options": [
            {"text": "將要做的事項輕重緩急排序一下，寫下每件事可能的解決方式，再一步一步去完成",
             "scores": {"悲": 0, "智": 2, "力": 1}},
            {"text": "先深呼吸、祈求、找老師朋友聊聊，總之先緩解自己內心的壓力", "scores": {"悲": 2, "智": 0, "力": 1}},
            {"text": "跟老師表達自己的現況，談談如何調整承擔的內容，以利長久的學習",
             "scores": {"悲": 0, "智": 3, "力": 0}}
        ]
    },
    {
        "id": 6,
        "image": "q6.jpg",
        "question": "白天上課、趕報告，晚上有小組討論，手機卻跳出社團群組的通知——活動流程需要確認，人力臨時有缺，大家都在等回覆.....",
        "options": [
            {"text": "翻開覆蓋的魔法卡，召喚其他人來幫忙", "scores": {"悲": 2, "智": 0, "力": 1}},
            {"text": "思考每件事情的關鍵，請適合的人協助解決", "scores": {"悲": 0, "智": 2, "力": 1}},
            {"text": "找到自己可以參與一點點的部分，貢獻螢火微光", "scores": {"悲": 1, "智": 0, "力": 2}}
        ]
    },
    {
        "id": 7,
        "image": "q7.jpg",
        "question": "周圍同學談著未來方向，我卻一片空白，心裡越來越慌，父母的建議接連而來，原本想被關心，卻只覺得煩躁又無力.....",
        "options": [
            {"text": "跟父母說「我不知道啦」，之後刻意避開相關話題，先不要去想未來的事。",
             "scores": {"悲": 0, "智": 0, "力": 0}},
            {"text": "正視自己對未來感到焦慮與迷惘，並主動為自己設定短期探索目標，例如蒐集資訊、找人聊經驗。",
             "scores": {"悲": 0, "智": 2, "力": 1}},
            {"text": "未來規劃本來就很現實，暫時把自己的情緒放一邊，父母總是為我好，就按父母建議走比較安全的路吧。",
             "scores": {"悲": 2, "智": 0, "力": 1}}
        ]
    },
    {
        "id": 8,
        "image": "q8.jpg",
        "question": "我有一個無話不談的好朋友，最近交了另一半，跟我的互動變得很少，也無法即時回應聊天，我不適應現在的感覺，覺得內心很失落...",
        "options": [
            {"text": "找個時機跟對方聊聊：「我最近有點不習慣我們變得比較少聊天，不知道你怎麼看？」",
             "scores": {"悲": 2, "智": 0, "力": 1}},
            {"text": "我太把情感重心放在對方身上，其實也讓自己很脆弱，確實應該要調整一下，找回一個平衡的身心狀態。",
             "scores": {"悲": 0, "智": 2, "力": 1}},
            {"text": "我沒有責怪他，但不再主動找他聊天，回覆也變得禮貌、簡短。我知道自己必須改變，什麼改變都好。",
             "scores": {"悲": 1, "智": 0, "力": 2}}
        ]
    }
]

# --- 計算每個向度的「理論最大分」 (分母) ---
# 邏輯：遍歷每一題，找出該題中「悲」最高的選項加總，就是「悲」的理論總分
MAX_POSSIBLE_SCORES = {"悲": 0, "智": 0, "力": 0}

for q in questions:
    # 針對每一題，找出悲、智、力個別選項中的最高分
    max_bei = max(opt['scores']['悲'] for opt in q['options'])
    max_zhi = max(opt['scores']['智'] for opt in q['options'])
    max_li = max(opt['scores']['力'] for opt in q['options'])

    MAX_POSSIBLE_SCORES['悲'] += max_bei
    MAX_POSSIBLE_SCORES['智'] += max_zhi
    MAX_POSSIBLE_SCORES['力'] += max_li

print("理論最大分數:", MAX_POSSIBLE_SCORES)
# 這樣我們就知道如果一個人全選悲最高的選項，總分會是多少


result_descriptions = {
    "悲": {
        "title": "慈悲關懷型 (Compassion)",
        "desc": "你擁有溫暖的心，總是優先考慮他人的感受。你是團體中的黏著劑，擅長同理與陪伴。",
        "color": "#FF9F68"  # 橘色
    },
    "智": {
        "title": "智慧思辨型 (Wisdom)",
        "desc": "你擅長理性分析與規劃，面對混亂能迅速理出頭緒。你是團體中的大腦，指引正確的方向。",
        "color": "#5D9BBA"  # 藍色
    },
    "力": {
        "title": "行動承擔型 (Power/Action)",
        "desc": "你坐言起行，擁有強大的執行力與意志。遇到困難時，你往往是第一個衝在前面解決問題的人。",
        "color": "#88C999"  # 綠色
    }
}


@app.route('/')
def home():
    session.clear()
    return render_template('index.html')


@app.route('/quiz/<int:question_idx>', methods=['GET', 'POST'])
def quiz(question_idx):
    if question_idx >= len(questions):
        return redirect(url_for('result'))

    if 'total_scores' not in session:
        session['total_scores'] = {"悲": 0, "智": 0, "力": 0}

    if request.method == 'POST':
        selected_option_index = int(request.form.get('option'))
        score_pack = questions[question_idx]['options'][selected_option_index]['scores']

        current_scores = session['total_scores']
        for key in score_pack:
            current_scores[key] += score_pack[key]

        session['total_scores'] = current_scores
        session.modified = True

        if question_idx + 1 < len(questions):
            return redirect(url_for('quiz', question_idx=question_idx + 1))
        else:
            return redirect(url_for('result'))

    current_question = questions[question_idx]
    progress_percent = ((question_idx + 1) / len(questions)) * 100

    return render_template('quiz.html',
                           question=current_question,
                           question_idx=question_idx,
                           progress=progress_percent)


@app.route('/result')
def result():
    user_scores = session.get('total_scores', {"悲": 0, "智": 0, "力": 0})

    # 1. 計算比例 (Ratio)
    # 避免分母為0的錯誤防呆
    ratios = {}
    for key in user_scores:
        denominator = MAX_POSSIBLE_SCORES.get(key, 1)  # 取得該項目的理論最高分
        if denominator == 0: denominator = 1
        ratios[key] = user_scores[key] / denominator

    # 2. 找出最大比例 (用來當作 10 分的基準)
    max_ratio = max(ratios.values())
    if max_ratio == 0: max_ratio = 1  # 避免除以0

    # 3. 換算成 10 分制圖表分數
    # 公式：(該項比例 / 最高項比例) * 10
    chart_scores = {}
    for key, ratio in ratios.items():
        chart_scores[key] = round((ratio / max_ratio) * 10, 2)

    # 4. 決定結果類型 (Winner)
    # 改用 "比例" 來決定誰是冠軍，而不是原始分數
    max_ratio_keys = [k for k, v in ratios.items() if v == max_ratio]
    winner_key = random.choice(max_ratio_keys)

    result_content = result_descriptions[winner_key]

    # 傳給前端的是 chart_scores (10分制)，但如果前端想顯示原始分數，也可以傳 user_scores
    return render_template('result.html',
                           result=result_content,
                           scores=chart_scores)  # 注意：這裡傳的是換算過的分數


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 1200))
    app.run(host='0.0.0.0', port=port)