# 先安装3-7行对应的库，输入190-194行对应的信息，运行代码即可查看爱斯维尔论文（under review之后）审稿进度。
# author:yxingg, 2025-02-13
import requests
import json
import uuid
import time
from collections import Counter, defaultdict

def generate_device_id():
    """生成一个设备ID"""
    return str(uuid.uuid4()).replace('-', '')[:32]

def get_manuscript_id(manuscript_number, last_name, first_name):
    url = 'https://dsp-api.elsevier.cn/st/manuscript/query-by-author'
    
    device_id = generate_device_id()
    
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/json',
        'Origin': 'https://webapps.elsevier.cn',
        'Referer': 'https://webapps.elsevier.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'X-Device-Id': device_id
    }
    
    data = {
        'manuscriptNumber': manuscript_number,
        'lastName': last_name,
        'firstName': first_name
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get('success') and result.get('code') == 200:
            manuscript_id = result.get('result', {}).get('manuscriptId')
            if manuscript_id:
                return manuscript_id
            else:
                raise Exception("响应中未找到manuscriptId")
        else:
            raise Exception(f"请求失败: {result.get('message', '未知错误')}")
            
    except Exception as e:
        raise Exception(f"获取manuscriptId失败: {str(e)}")

def get_manuscript_uuid(manuscript_id):
    """根据manuscriptId获取uuid"""
    url = f'https://dsp-api.elsevier.cn/st/site/manuscript/v2/detail'
    
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Origin': 'https://webapps.elsevier.cn',
        'Referer': 'https://webapps.elsevier.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }
    
    # 添加id作为查询参数
    params = {
        'id': manuscript_id
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()
        
        if result.get('success') and result.get('code') == 200:
            uuid = result.get('result', {}).get('uuid')
            if uuid:
                return uuid
            else:
                raise Exception("响应中未找到uuid")
        else:
            raise Exception(f"请求失败: {result.get('message', '未知错误')}")
            
    except Exception as e:
        raise Exception(f"获取uuid失败: {str(e)}")

def trans(tt):
    """时间戳转换为时间"""
    s_l = time.localtime(tt)
    return time.strftime("%Y-%m-%d %H:%M:%S", s_l)

def merge_continuous_ids(events):
    """合并同一时间点的连续ID"""
    # 按时间和事件类型分组
    grouped_events = defaultdict(list)
    for event in events:
        key = (event['Date'], event['Event'])
        grouped_events[key].append(event)
    
    merged_events = []
    for (date, event_type), group in grouped_events.items():
        if len(group) > 1:
            # 检查ID是否连续
            ids = sorted([event['Id'] for event in group])
            merged_id = []
            start = ids[0]
            prev = start
            
            for curr in ids[1:] + [None]:
                if curr is None or curr != prev + 1:
                    if prev == start:
                        merged_id.append(str(start))
                    else:
                        merged_id.append(f"{str(start)[:-2]}{str(start)[-2:]}-{str(prev)[-2:]}")
                    start = curr
                prev = curr
            
            # 创建合并后的事件
            merged_event = group[0].copy()
            merged_event['Id'] = ', '.join(merged_id)
            merged_events.append(merged_event)
        else:
            merged_events.append(group[0])
    
    return sorted(merged_events, key=lambda x: x['Date'])

def format_paper_info(data):
    """格式化论文基本信息"""
    print("\n" + "="*60)
    print("论文基本信息".center(56))
    print("="*60)
    print(f"论文标题: {data['ManuscriptTitle']}")
    print(f"投稿编号: {data['PubdNumber']}")
    print(f"期刊名称: {data['JournalName']} ({data['JournalAcronym']})")
    print(f"第一作者: {data['FirstAuthor']}")
    print(f"通讯作者: {data['CorrespondingAuthor']}")
    print(f"投稿时间: {trans(data['SubmissionDate'])}")
    print(f"最近更新: {trans(data['LastUpdated'])}")
    print(f"当前修改版本: R{data['LatestRevisionNumber']}")

def get_event_name(event_type):
    """转换事件类型为中文"""
    event_map = {
        'REVIEWER_INVITED': '邀请审稿人',
        'REVIEWER_ACCEPTED': '已接受审稿',
        'REVIEWER_COMPLETED': '已完成审稿'
    }
    return event_map.get(event_type, event_type)

def format_review_events(data):
    """格式化审稿事件信息"""
    print("\n" + "="*60)
    print("审稿进度信息".center(56))
    print("="*60)
    
    # 按版本分组
    review_events = data['ReviewEvents']
    version_groups = defaultdict(list)
    for event in review_events:
        version_groups[event['Revision']].append(event)
    
    # 对每个版本进行统计和显示
    for revision in sorted(version_groups.keys()):
        print(f"\nR{revision} 版本:")
        print("-"*60)
        
        # 统计当前版本的事件数量
        events = version_groups[revision]
        event_counter = Counter(event['Event'] for event in events)
        
        print(f"审稿状态统计:")
        print(f"已邀请审稿人数: {event_counter['REVIEWER_INVITED']}")
        print(f"已接受审稿人数: {event_counter.get('REVIEWER_ACCEPTED', 0)}")
        print(f"已完成审稿人数: {event_counter.get('REVIEWER_COMPLETED', 0)}")
        
        print(f"\n详细审稿过程:")
        print("-"*60)
        print(f"{'时间':^19} | {'事件':^12} | {'版本':^6} | {'ID':^15}")
        print("-"*60)
        
        # 合并连续ID并显示
        merged_events = merge_continuous_ids(events)
        for event in merged_events:
            event_type = get_event_name(event['Event'])
            print(f"{trans(event['Date']):19} | {event_type:^12} | {f'R{event['Revision']}':^6} | {event['Id']:^15}")

def main():
    try:
        # 获取manuscriptId
        manuscript_id = get_manuscript_id(
            manuscript_number="",# 引号内填论文编号，如JII-D-xx-xxxxx
            last_name="",# 引号内填通讯作者姓
            first_name=""# 引号内填通讯作者名
        )
        
        # 获取uuid
        uuid = get_manuscript_uuid(manuscript_id)
        
        # 获取论文进度
        url = f'https://tnlkuelk67.execute-api.us-east-1.amazonaws.com/tracker/{uuid}'
        res = requests.get(url)
        data = json.loads(res.text)
        
        # 格式化输出
        format_paper_info(data)
        format_review_events(data)
        
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()