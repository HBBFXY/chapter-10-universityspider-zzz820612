import requests
from bs4 import BeautifulSoup
import time

def get_html(url):
    """获取网页内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        return response.text
    except:
        return ""

def parse_university_data(html):
    """解析大学数据"""
    soup = BeautifulSoup(html, 'html.parser')
    universities = []
    
    # 查找所有表格行
    rows = soup.find_all('tr')
    
    for row in rows:
        # 查找所有单元格
        cells = row.find_all('td')
        
        # 确保有足够的单元格
        if len(cells) >= 4:
            # 提取数据，使用更安全的方法
            rank = cells[0].text.strip() if cells[0].text else ""
            name = cells[1].text.strip() if cells[1].text else ""
            province = cells[2].text.strip() if cells[2].text else ""
            score = cells[3].text.strip() if cells[3].text else ""
            
            # 只添加有效数据
            if rank and name:
                universities.append([rank, name, province, score])
    
    return universities

def main():
    """主函数"""
    all_universities = []
    
    # 软科中国大学排名URL
    base_url = " https://www.shanghairanking.cn/rankings/bcur/2023 "
    
    print("开始爬取中国大学排名...")
    
    # 爬取多页数据
    for page in range(1, 31):  # 假设有30页
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page}"
        
        print(f"正在处理第 {page} 页...")
        
        html = get_html(url)
        if html:
            page_data = parse_university_data(html)
            all_universities.extend(page_data)
            print(f"  获取到 {len(page_data)} 条记录")
        else:
            print(f"  第 {page} 页获取失败")
        
        # 延迟避免被封
        time.sleep(1)
    
    # 显示结果
    print(f"\n总共获取了 {len(all_universities)} 所大学的信息")
    
    if all_universities:
        # 显示前20名
        print("\n前20名大学：")
        print("-" * 70)
        print(f"{'排名':<6}{'学校名称':<30}{'省市':<15}{'总分':<10}")
        print("-" * 70)
        
        for i in range(min(20, len(all_universities))):
            uni = all_universities[i]
            print(f"{uni[0]:<6}{uni[1]:<30}{uni[2]:<15}{uni[3]:<10}")
        
        # 保存到文件
        with open('universities.txt', 'w', encoding='utf-8') as f:
            f.write("排名,学校名称,省市,总分\n")
            for uni in all_universities:
                f.write(f"{uni[0]},{uni[1]},{uni[2]},{uni[3]}\n")
        
        print(f"\n数据已保存到 universities.txt")

if __name__ == "__main__":
    main()
# 在这里编写代码
