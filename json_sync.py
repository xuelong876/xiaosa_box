import os
import json
import requests
from typing import List, Dict

# 配置区
CONFIG = {
    "xiaosa_json_url": "https://raw.githubusercontent.com/qist/tvbox/refs/heads/master/xiaosa/api.json",
    "wallpaper": "http://饭太硬.top/深色壁纸/api.php",
    "logo": "https://raw.giteeusercontent.com/xuelong88/xiaosa_box/raw/master/pg.gif",
    "spider": "https://gitee.com/xuelong88/xiaosa_box/raw/master/spider.jar",
    # 关键修改：默认输出到仓库根目录的 xiaosa.json
    # 本地想写到 C:\C盘下载\... 时，设置环境变量 XIAOSA_OUTPUT 即可
    "output_path": os.environ.get(
        "XIAOSA_OUTPUT",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "xiaosa.json",
        ),
    ),
    "exclude_names": [
        "短剧", "123", "戏曲", "本地", "抖音", "推送", "预告", "动漫",
        "看球", "DJ", "体育", "听书", "FM", "儿童", "童趣", "课堂",
        "教育", "急救", "养生", "知识",
    ],
    "add_site": [
        {
            "key": "腾讯视频",
            "name": "🎬腾讯｜视频🍅",
            "type": 3,
            "api": "https://raw.giteeusercontent.com/xuelong88/xiaosa_box/raw/master/xiaosa/drpy2.min.js",
            "ext": "https://raw.giteeusercontent.com/xuelong88/xiaosa_box/raw/master/xiaosa/腾讯视频.js",
            "changeable": 0,
        },
        {
            "key": "优酷视频",
            "name": "🎬优酷｜视频🍅",
            "type": 3,
            "api": "https://raw.giteeusercontent.com/xuelong88/xiaosa_box/raw/master//xiaosa/drpy2.min.js",
            "ext": "https://raw.giteeusercontent.com/xuelong88/xiaosa_box/raw/master/xiaosa/优酷视频.js",
            "changeable": 0,
        },
        {
            "key": "芒果视频",
            "name": "🎬芒果｜视频🍅",
            "type": 3,
            "api": "https://raw.giteeusercontent.com/xuelong88/xiaosa_box/raw/master/xiaosa/drpy2.min.js",
            "ext": "https://raw.giteeusercontent.com/xuelong88/xiaosa_box/raw/master/xiaosa/芒果视频.js",
            "changeable": 0,
        },
        {
            "key": "爱奇艺",
            "name": "🎬爱奇艺｜视频🍅",
            "type": 3,
            "api": "https://raw.giteeusercontent.com/xuelong88/xiaosa_box/raw/master/xiaosa/drpy2.min.js",
            "ext": "https://raw.giteeusercontent.com/xuelong88/xiaosa_box/raw/master/xiaosa/爱奇艺.js",
            "changeable": 0,
        },
        {
            "key": "猎手影视",
            "name": "🏂猎手｜py🍅 ",
            "type": 3,
            "api": "./py/猎手影视.py",
            "searchable": 1,
            "changeable": 0,
            "quickSearch": 1,
            "filterable": 1,
        },
    ],
    "lives": [
        {
            "name": "移动8m",
            "type": 0,
            "url": "https://gh-proxy.com/https://raw.githubusercontent.com/xuelong876/mybox_PG/refs/heads/main/live/YD8M.m3u",
            "playerType": 2,
            "ua": "okhttp/3.12.13",
            "logo": "https://cdn.jsdelivr.net/gh/xuelong876/channal_logo2@master/{name}.png",
            "epg": "http://cdn.1678520.xyz/epg/?ch={name}&date={date}",
        },
        {
            "name": "刺桐自营",
            "type": 0,
            "url": "https://www.cttv.vip/ys/json/ctzb.txt",
            "playerType": 2,
            "ua": "okhttp/3.12.13",
            "logo": "https://cdn.jsdelivr.net/gh/xuelong876/channal_logo2@master/{name}.png",
            "epg": "http://cdn.1678520.xyz/epg/?ch={name}&date={date}",
        },
    ],
}

# --- 名称美化（添加Emoji）---
def add_emoji_to_name(name: str) -> str:
    """添加Emoji到名称，按列表顺序依次判断，命中第一条即返回"""
    rules = [
        ("startswith", "豆瓣", "🏠豆瓣 • 潇洒👨"),
        ("startswith", "配置", "⚙️配置 • 中心🍅"),
        ("startswith", "哔哩", "🅱️{name}🍅"),
        ("endswith", "APP", "🐞{name}🍅"),
        ("endswith", "视频", "🎬{name}🍅"),
        ("endswith", "影视", "🎥{name}🍅"),
        ("endswith", ("4K", "网盘", "云盘"), "☁{name}🍅"),
        ("endswith", "磁力", "🧲{name}🍅"),
        ("endswith", "搜索", "🔍 {name}🍅"),
    ]

    if not isinstance(name, str) or not name:
        return ""

    for match_type, match_val, template in rules:
        if match_type == "startswith":
            if name.startswith(match_val):
                return template.format(name=name) if "{name}" in template else template
        elif match_type == "endswith":
            if isinstance(match_val, tuple):
                if any(name.endswith(val) for val in match_val):
                    return template.format(name=name)
            elif name.endswith(match_val):
                return template.format(name=name)

    return f"🍅{name}🍅"


def main():
    """
    1. 读取接口 JSON
    2. 修改壁纸、logo、spider
    3. 替换 lives
    4. 过滤 sites 中的站点
    5. 给站点 name 加 Emoji
    6. 追加 add_site
    7. 保存到指定路径
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(
            CONFIG["xiaosa_json_url"], timeout=15, headers=headers
        )
        response.raise_for_status()
        data = response.json()

        # 修改基本字段
        data["wallpaper"] = CONFIG["wallpaper"]
        data["logo"] = CONFIG["logo"]
        data["spider"] = CONFIG["spider"]

        # 替换 lives
        data["lives"] = CONFIG["lives"]

        # 过滤 + 美化 sites
        if "sites" in data and isinstance(data["sites"], list):
            data["sites"] = [
                site
                for site in data["sites"]
                if not any(
                    exclude_name in site.get("name", "")
                    for exclude_name in CONFIG["exclude_names"]
                )
            ]

            for site in data["sites"]:
                name = site.get("name", "")
                if name:
                    site["name"] = add_emoji_to_name(name)
                site["changeable"] = 0
        else:
            data["sites"] = []

        # 追加自定义站点
        data["sites"].extend(CONFIG["add_site"])

        # 确保输出目录存在
        output_path = CONFIG["output_path"]
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 写文件
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"处理完成，文件已保存到：{output_path}")

    except requests.exceptions.RequestException as e:
        print(f"网络请求错误：{e}")
        raise SystemExit(1)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"处理过程中发生错误：{e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()