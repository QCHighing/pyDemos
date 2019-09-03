import os
import requests  # HTTP
import re  # 正则表达式
import test  # 网页爬虫调试
import unixtime  # Unix时间戳
import download  # 文件下载
from urllib.parse import quote  # URL编码解码
from prettytable import PrettyTable, FRAME, NONE  # 表格输出


# 搜索页面相关的全局变量
pageIndex = 0           # 页码
totlePageCount = 0      # 总页数
curPageCount = 0        # 当前页的课程数
totleCount = 0          # 搜索到的总课程数
courseIndex = 0         # 课程编号

# 请求头
headers = {'Host': 'www.icourse163.org',
           'Connection': 'keep-alive',
           'Origin': 'https://www.icourse163.org',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           'Content-Type': 'text/plain'}


# 搜索课程，爬取搜索结果页面
def search_course(keyword, pageIndex=1):
    url = 'https://www.icourse163.org/dwr/call/plaincall/MocSearchBean.searchMocCourse.dwr'
    status = 30
    pageSize = 20
    data = {'callCount': '1',
            'scriptSessionId': '${scriptSessionId}190',
            'httpSessionId': 'bd4f183dd74746aa83b2cced56a0795b',
            'c0-scriptName': 'MocSearchBean',
            'c0-methodName': 'searchMocCourse',
            'c0-id': '0',
            'c0-e1': 'string:' + quote(keyword),
            'c0-e2': 'number:{}'.format(pageIndex),
            'c0-e3': 'boolean:true',
            'c0-e4': 'null:null',
            'c0-e5': 'number:0',
            'c0-e6': 'number:{}'.format(status),  # 0-已结束; 10-正在进行; 20-即将开始; 30-所有课程
            'c0-e7': 'number:{}'.format(pageSize),
            'c0-param0': 'Object_Object:{keyword:reference:c0-e1,pageIndex:reference:c0-e2,highlight:reference:c0-e3,categoryId:reference:c0-e4,orderBy:reference:c0-e5,stats:reference:c0-e6,pageSize:reference:c0-e7}',
            'batchId': '1528898317310'}
    # test.printDICT(data)      # 测试所用
    try:
        r = requests.post(url, headers=headers, data=data)
        r.raise_for_status()
        # test.detect_encoding(r)  # 检测到响应的编码时'ascii'
        page = r.text.encode('utf-8').decode('unicode_escape')  # 解码为 unicode_escape 便于print将汉字打印输出
        # print(page[3000:4000])    # 测试所用
        # test.outputHTML(page, '搜索页面第 ' + str(pageIndex) + ' 页')
        return page
    except requests.HTTPError as ex:
        print('课程搜索页面访问出错...\n[-]ERROR: %s' % str(ex))
        raise


# 解析搜索结果的页面
def parse_search(page):
    # 页面信息解析
    global pageIndex, totleCount, totlePageCount, curPageCount
    # 搜索结果统计
    re_pageInfo = r'pageIndex=(\d+);.*totleCount=(\d+);.*totlePageCount=(\d+);'
    list_pageInfo = re.findall(re_pageInfo, page[-10000:])  # 得到一个多维列表形式的匹配结果
    if len(list_pageInfo) == 0:
        print("未爬取到相关信息，请根据搜索页面修正 Regular Expression")
        test.outputHTML(searchPage, "搜索页面")
        return None, None
    pageIndex = int(list_pageInfo[0][0])
    totleCount = int(list_pageInfo[0][1])
    totlePageCount = int(list_pageInfo[0][2])
    # 课程信息解析
    # 0 - cid(无用);  1 - 课程名;    2 - 授课教师;    3 - 院校;    4 - tid,termId
    page = re.sub(r'({##)|(##})', '', page)  # 删除page中的#{}符号
    re_courseInfo = r'cid=(\d+);.*highlightName="(.+)";.*highlightTeacherNames="(.+)";.*highlightUniversity="(.+)";' \
                    r'.+\W{0,4}.+currentTermId=(\d+);'
    list_courseInfo = re.findall(re_courseInfo, page)
    # 课程状态解析
    # 0 - 结束时间;  1 - 参加人数;    2 - 介绍    3 - 开始时间;
    re_courseStat = r'endTime=(\d+);.*?enrollCount=(\d+);.*?jsonContent="(.+[\s\S]{0,120}.+)";.*startTime=(\d+);'
    list_courseStat = re.findall(re_courseStat, page)
    curPageCount = len(list_courseInfo)
    return list_courseInfo, list_courseStat


# 输出搜索到的页面信息与课程列表
def disp_search(courseInfo):
    print('>>> 搜索到 %d 条相关结果\t\t当前第 %d 页\t\t共 %d 页\t\t向上翻页:[u]\t\t向下翻页:[d]\t\t重新搜索:[e]' %
          (totleCount, pageIndex, totlePageCount))
    table = PrettyTable([' ', "编号", "课程名（ 输入序号查看详情 ）", "授课教师", "开设院校"])
    table.align = 'l'
    table.vrules = FRAME
    table.vertical_char = ' '
    table.align["授课教师"] = 'c'
    table.align["开设院校"] = 'c'
    for i, item in zip(range(curPageCount), courseInfo):
        table.add_row([' ', i, item[1][:20], item[2][:11], item[3][:10]])
    print(table)
    # print('当前页%d条' % curPageCount)


# 交互
def user_interface(courseInfo, courseStat, courseName=[]):
    global pageIndex, courseIndex
    while True:
        cmd = input('>>> 请输入命令(课程编号/u/d/e)：').strip()
        if re.match(r'^\d\d?\W*$', cmd):
            courseIndex = eval(cmd)
            if 0 <= courseIndex <= curPageCount:
                try:
                    courseName.append(courseInfo[courseIndex][1].strip())
                    courseAbstract = courseStat[courseIndex][2]
                    startTime = unixtime.number2time(courseStat[courseIndex][3], 13)
                    endTime = unixtime.number2time(courseStat[courseIndex][0], 13)
                    enrollCount = courseStat[courseIndex][1]
                    print('>>>', courseName[0], '：', courseAbstract, '\n')
                    print('\t开课时间：%s\n\t结束时间：%s\n\t已参加人数：%s\n' % (startTime, endTime, enrollCount))
                except:
                    print('>>> 该课程暂未开通，请访问以下链接进行确认！')
                    print('>>> https://www.icourse163.org/search.htm?search={}#/'.format(quote(courseName[0])))
                    main()
                cmd = input('>>> 按下Enter键选定该课程，退出选定请按其他键： ')
                if re.match(r'^.*?\n*$', cmd, re.I):
                    cmd = input('>>> 下载视频(v)还是课件(p)？退出下载请按其他键： ')  # 3代表文档，1代表视频
                    if re.match(r'^v\W*$', cmd, re.I):
                        print('>>> 正在进行视频资源分析，请稍后...')
                        return 1
                    elif re.match(r'^p\W*$', cmd, re.I):
                        print('>>> 正在进行课件资源分析，请稍后...')
                        return 3
                    else:
                        print('>>> 已退出下载！')
                else:
                    print('>>> 已退出选定！')
            else:
                print('>>> 课程编号输入错误，请重新输入！')
        elif re.match(r'^e\W*$', cmd, re.I):
            main()
        elif re.match(r'^u\W*$', cmd, re.I):
            if pageIndex <= 1:
                print('>>> 已经是首页了...')
            else:
                pageIndex -= 1
                break
        elif re.match(r'^d\W*$', cmd, re.I):
            if pageIndex >= totlePageCount:
                print('>>> 已经是尾页了...')
            else:
                pageIndex += 1
                break
        else:
            print('>>> 命令错误，请重新输入！')
    return False  # 刷新搜索页面


# 获取资源页列表
def get_source_list(tid):
    # 2018.6 抓取的数据包没有 getMocTermDto.dwr，怀疑是MOOC改版了。只能通过查getLastLearnedMocTermDto.dwr得到资源列表
    # 但是这就需要加入Cookie了，还要保持对话什么的...不是很方便，就暂时还用网络大神的老版本吧
    # url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLastLearnedMocTermDto.dwr'  # POST请求，视频链接在r的js中
    url = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getMocTermDto.dwr'  # 网络大神的旧链接
    data = {'callCount': '1',
            'scriptSessionId': '${scriptSessionId}190',
            'c0-scriptName': 'CourseBean',
            'c0-methodName': 'getMocTermDto',
            'c0-id': 0,
            'c0-param0': 'number:' + tid,  # tid,termId
            'c0-param1': 'number:1',
            'c0-param2': 'boolean:true',
            'batchId': unixtime.now()}
    try:
        r = requests.post(url, headers=headers, data=data)
        r.raise_for_status()
        # test.detect_encoding(r)  # 检测到响应的编码时'ascii'
        page = r.text.encode('utf-8').decode('unicode_escape')  # 解码为 unicode_escape 便于print将汉字打印输出
        # print(page[3000:4000])    # 测试所用
        # test.outputHTML(page, '获取资源列表')
        return page
    except requests.HTTPError as ex:
        print('>>> 课程搜索页面访问出错...\n[-]ERROR: %s' % str(ex))
        raise


# 解析资源页列表，得到下载请求的data包参数：contentId,contentType(传入),文件id,文件name
def parse_source(page, sourceType):
    # 3代表文档，1代表视频
    ch = '段视频' if sourceType is 1 else '份课件'
    # 0 - cid;      1 - id;     2 - name
    re_sourceList = r'anchorQuestions=.*contentId=(\d*);.*contentType={};.*id=(\d*);.*name="(.*)";'.format(
        sourceType)
    sourceList = re.findall(re_sourceList, page)
    if not sourceList:
        print('>>> Source List is Empty!')
    else:
        print('>>> 本课程共有', len(sourceList), ch, end=',')
    return sourceList


# 解析下载链接: 1代表视频, 3代表文档
def get_download_info(dataList, sourceType, Quality=None, fileFormat=None):
    url = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
    content_id = dataList[0]
    file_id = dataList[1]
    file_name = re.sub(r'[/\\*|<>:?"]', '', dataList[2])  # 移除Windows文件名非法字符
    data = {'callCount': '1',
            'scriptSessionId': '${scriptSessionId}190',
            'c0-scriptName': 'CourseBean',
            'c0-methodName': 'getLessonUnitLearnVo',
            'c0-id': '0',
            'c0-param0': 'number:' + content_id,  # contentId
            'c0-param1': 'number:{}'.format(sourceType),
            'c0-param2': 'number:0',
            'c0-param3': 'number:' + file_id,  # 文件id
            'batchId': unixtime.now()}
    try:
        r = requests.post(url, headers=headers, data=data)
        r.raise_for_status()
        page = r.text
        # test.outputHTML(page,'下载链接')
    except requests.HTTPError as ex:
        print('课程搜索页面访问出错...\n[-]ERROR: %s' % str(ex))
        raise
    if Quality:  # 进行视频文件的解析
        re_videoLink = r'{}{}Url="(.+?)";'.format(fileFormat, Quality)
        video_url = re.findall(re_videoLink, page)
        re_srtLink = r's\d+\.name="([\w\\]+?)";s\d+\.url="(.+?)";'
        srt_url = re.findall(re_srtLink, page)
        if video_url:
            if srt_url:
                return [video_url[0], srt_url[0][1]], file_name
            else:
                return [video_url[0]], file_name
        else:
            return [], file_name
    else:  # 进行课件文件的解析
        re_PDFLink = r'http://nos.netease.com/.*?\.pdf'
        pdf_url = re.findall(re_PDFLink, page)
        if pdf_url:
            return [pdf_url[0]], file_name
        else:
            return [], file_name


# 批量下载所有资源: 1代表视频, 3代表文档
def mass_dowmload(sourceList, sourceType, courseName):
    download_cnt = 0
    direction = download.select_direction(courseName)
    if sourceType is 1:  # 视频下载
        qualityList = ['Hd', 'Sd', 'Shd', 'Hd', 'Sd', 'Shd']
        formatList = ['flv', 'flv', 'flv', 'mp4', 'mp4', 'mp4']
        while True:
            index = input('>>> 请选择视频格式：\n\t0-FLV高清，1-FLV标清，2-FLV超清\n\t3-MP4高清，4-MP4标清，5-MP4超清\n>>> ')
            if re.match(r'\d', index):
                index = int(index)  # 将字符串数字转为数值
                if 0 <= index <= 5:
                    quality = qualityList[index]
                    fileFormat = formatList[index]
                    break
            else:
                print('>>> 选择错误！')
    else:
        quality = None
        fileFormat = 'pdf'
    skipNum = input('>>> 如需断点下载，请输入跳过的文件数，否则请按Enter键：')
    if re.match(r'\d', skipNum):
        skipNum = int(skipNum)
    else:
        skipNum = 0
    for item in sourceList:
        download_cnt += 1
        if download_cnt <= skipNum:
            continue
        (url, name) = get_download_info(item, sourceType, quality, fileFormat)
        print(f'\n[+]正在下载第{download_cnt}份 - {name}.{fileFormat} ...\n')
        if len(url) is 1:
            download.download(url[0], direction, name, fileFormat)  # 课件或课件
        elif len(url) is 2:
            download.download(url[0], direction, name, fileFormat)  # 视频
            download.download(url[1], direction, name, 'srt', 'smallfile')  # 字幕
        else:
            print('[-]ERROR:URL is None')
    print('\n>>> 下载完成！本次总计下载资源{}份'.format(download_cnt))


# 主函数
def main():
    keyword = input('>>> 请输入关键字搜索课程：')
    # keyword = test.inputString('机器学习')
    global pageIndex
    pageIndex = 1
    while True:
        searchPage = search_course(keyword, pageIndex)
        (courseInfo, courseStat) = parse_search(searchPage)
        if courseInfo is None:
            break
        disp_search(courseInfo)
        courseName = []
        download_type = user_interface(courseInfo, courseStat, courseName)
        if download_type:
            sourcePage = get_source_list(courseInfo[courseIndex][4])
            sourceList = parse_source(sourcePage, download_type)
            if sourceList:
                cmd = input('请按下Enter键确认下载，取消请按其他键: ')
                if re.match(r'^.*\n*$', cmd, re.I):
                    mass_dowmload(sourceList, download_type, courseName[0])
                else:
                    print('>>> 已退出下载！')
                break
    os.system("pause")


if __name__ == '__main__':
    main()
