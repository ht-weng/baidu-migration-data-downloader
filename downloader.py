# Note that Baidu only provides data for 2020

# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timedelta
from datetime import date as dtdate
import json
import time
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


city_code = {
    '北京市':110000, 
    '天津市':120000, 
    '石家庄市':130100, '唐山市':130200, '秦皇岛市':130300, '邯郸市':130400, '邢台市':130500, '保定市':130600, '张家口市':130700, '承德市':130800, '沧州市':130900, '廊坊市':131000, '衡水市':131100, 
    '太原市':140100, '大同市':140200, '阳泉市':140300, '长治市':140400, '晋城市':140500, '朔州市':140600, '晋中市':140700, '运城市':140800, '忻州市':140900, '临汾市':141000, '吕梁市':141100, 
    '呼和浩特市':150100, '包头市':150200, '乌海市':150300, '赤峰市':150400, '通辽市':150500, '鄂尔多斯市':150600, '呼伦贝尔市':150700, '巴彦淖尔市':150800, '乌兰察布市':150900, '兴安盟':152200, '锡林郭勒盟':152500, '阿拉善盟':152900, 
    '沈阳市':210100, '大连市':210200, '鞍山市':210300, '抚顺市':210400, '本溪市':210500, '丹东市':210600, '锦州市':210700, '营口市':210800, '阜新市':210900, '辽阳市':211000, '盘锦市':211100, '铁岭市':211200, '朝阳市':211300, '葫芦岛市':211400, 
    '长春市':220100, '吉林市':220200, '四平市':220300, '辽源市':220400, '通化市':220500, '白山市':220600, '松原市':220700, '白城市':220800, '延边朝鲜族自治州':222400, 
    '哈尔滨市':230100, '齐齐哈尔市':230200, '鸡西市':230300, '鹤岗市':230400, '双鸭山市':230500, '大庆市':230600, '伊春市':230700, '佳木斯市':230800, '七台河市':230900, '牡丹江市':231000, '黑河市':231100, '绥化市':231200, '大兴安岭地区':232700, 
    '上海市':310000, 
    '南京市':320100, '无锡市':320200, '徐州市':320300, '常州市':320400, '苏州市':320500, '南通市':320600, '连云港市':320700, '淮安市':320800, '盐城市':320900, '扬州市':321000, '镇江市':321100, '泰州市':321200, '宿迁市':321300, 
    '杭州市':330100, '宁波市':330200, '温州市':330500, '嘉兴市':330400, '湖州市':330500, '绍兴市':330600, '金华市':330700, '衢州市':330800, '舟山市':330900, '台州市':331000, '丽水市':331100, 
    '合肥市':340100, '芜湖市':340200, '蚌埠市':340300, '淮南市':340400, '马鞍山市':340500, '淮北市':340600, '铜陵市':340700, '安庆市':340800, '黄山市':341000, '滁州市':341100, '阜阳市':341200, '宿州市':341300, '六安市':341500, '亳州市':341600, '池州市':341700, '宣城市':341800, 
    '福州市':350100, '厦门市':350200, '莆田市':350300, '三明市':350400, '泉州市':350500, '漳州市':350600, '南平市':350700, '龙岩市':350800, '宁德市':350900, 
    '南昌市':360100, '景德镇市':360200, '萍乡市':360300, '九江市':360400, '新余市':360500, '鹰潭市':360600, '赣州市':360700, '吉安市':360800, '宜春市':360900, '抚州市':361000, '上饶市':361100, 
    '济南市':370100, '青岛市':370200, '淄博市':370300, '枣庄市':370400, '东营市':370500, '烟台市':370600, '潍坊市':370700, '济宁市':370800, '泰安市':370900, '威海市':371000, '日照市':371100, '临沂市':371300, '德州市':371400, '聊城市':371500, '滨州市':371600, '菏泽市':371700, 
    '郑州市':410100, '开封市':410200, '洛阳市':410300, '平顶山市':410400, '安阳市':410500, '鹤壁市':410600, '新乡市':410700, '焦作市':410800, '濮阳市':410900, '许昌市':411000, '漯河市':411100, '三门峡市':411200, '南阳市':411300, '商丘市':411400, '信阳市':411500, '周口市':411600, '驻马店市':411700, '济源市':419001, 
    '武汉市':420100, '黄石市':420200, '十堰市':420300, '宜昌市':420500, '襄阳市':420600, '鄂州市':420700, '荆门市':420800, '孝感市':420900, '荆州市':421000, '黄冈市':421100, '咸宁市':421200, '随州市':421300, '恩施土家族苗族自治州':422800, '仙桃市':429004, '潜江市':429005, '天门市':429006, '神农架林区':429021, 
    '长沙市':430100, '株洲市':430200, '湘潭市':430300, '衡阳市':430400, '邵阳市':430500, '岳阳市':430600, '常德市':430700, '张家界市':430800, '益阳市':430900, '郴州市':431000, '永州市':431100, '怀化市':431200, '娄底市':431300, '湘西土家族苗族自治州':433100, 
    '广州市':440100, '韶关市':440200, '深圳市':440300, '珠海市':440400, '汕头市':440500, '佛山市':440600, '江门市':440700, '湛江市':440800, '茂名市':440900, '肇庆市':441200, '惠州市':441300, '梅州市':441400, '汕尾市':441500, '河源市':441600, '阳江市':441700, '清远市':441800, '东莞市':441900, '中山市':442000, '潮州市':445100, '揭阳市':445200, '云浮市':445300, 
    '南宁市':450100, '柳州市':450200, '桂林市':450300, '梧州市':450400, '北海市':450500, '防城港市':450600, '钦州市':450700, '贵港市':450800, '玉林市':450900, '百色市':451000, '贺州市':451100, '河池市':451200, '来宾市':451300, '崇左市':451400, 
    '海口市':460100, '三亚市':460200, '三沙市':460300, '儋州市':460400, '五指山市':469001, '琼海市':469002, '文昌市':469005, '万宁市':469006, '东方市':469007, '定安县':469021, '屯昌县':469022, '澄迈县':469023, '临高县':469024, '白沙黎族自治县':469025, '昌江黎族自治县':469026, '乐东黎族自治县':469027, '陵水黎族自治县':469028, '保亭黎族苗族自治县':469029, '琼中黎族苗族自治县':469030, 
    '重庆市':500000, 
    '成都市':510100, '自贡市':510300, '攀枝花市':510400, '泸州市':510500, '德阳市':510600, '绵阳市':510700, '广元市':510800, '遂宁市':510900, '内江市':511000, '乐山市':511100, '南充市':511300, '眉山市':511400, '宜宾市':511500, '广安市':511600, '达州市':511700, '雅安市':511800, '巴中市':511900, '资阳市':512000, '阿坝藏族羌族自治州':513200, '甘孜藏族自治州':513300, '凉山彝族自治州':513400, 
    '贵阳市':520100, '六盘水市':520200, '遵义市':520300, '安顺市':520400, '毕节市':520500, '铜仁市':520600, '黔西南州':522300, '黔东南州':522600, '黔南州':522700, 
    '昆明市':530100, '曲靖市':530300, '玉溪市':530400, '保山市':530500, '昭通市':530600, '丽江市':530700, '普洱市':530800, '临沧市':530900, '楚雄彝族自治州':532300, '红河哈尼族彝族自治州':532500, '文山壮族苗族自治州':532600, '西双版纳傣族自治州':532800, '大理白族自治州':532900, '德宏傣族景颇族自治州':533100, '怒江傈僳族自治州':533300, '迪庆藏族自治州':533400, 
    '拉萨市':540100, '日喀则市':540200, '昌都市':540300, '林芝市':540400, '山南市':540500, '那曲市':540600, '阿里地区':542500, 
    '西安市':610100, '铜川市':610200, '宝鸡市':610300, '咸阳市':610400, '渭南市':610500, '延安市':610600, '汉中市':610700, '榆林市':610800, '安康市':610900, '商洛市':611000, 
    '兰州市':620100, '嘉峪关市':620200, '金昌市':620300, '白银市':620400, '天水市':620500, '武威市':620600, '张掖市':620700, '平凉市':620800, '酒泉市':620900, '庆阳市':621000, '定西市':621100, '陇南市':621200, '临夏州':622900, '甘南州':623000, 
    '西宁市':630100, '海东市':630200, '海北藏族自治州':632200, '黄南藏族自治州':632300, '海南藏族自治州':632500, '果洛藏族自治州':632600, '玉树藏族自治州':632700, '海西蒙古族藏族自治州':632800, 
    '银川市':640100, '石嘴山市':640200, '吴忠市':640300, '固原市':640400, '中卫市':640500, 
    '乌鲁木齐市':650100, '克拉玛依市':650200, '吐鲁番市':650400, '哈密市':650500, '昌吉回族自治州':652300, '博尔塔拉蒙古自治州':652700, '巴音郭楞蒙古自治州':652800, '阿克苏地区':652900, '克孜勒苏柯尔克孜自治州':653000, '喀什地区':653100, '和田地区':653200, '伊犁哈萨克自治州':654000, '塔城地区':654200, '阿勒泰地区':654300, 
    '石河子市':659001, '阿拉尔市':659002, '图木舒克市':659003, '五家渠市':659004, '北屯市':659005, '铁门关市':659006, '双河市':659007, '可克达拉市':659008, '昆玉市':659009, 
    '台湾省':710000, 
    '香港特别行政区':810000, 
    '澳门特别行政区':820000
}

city_name = {
    '北京市':'Beijing', 
    '天津市':'Tianjin', 
    '石家庄市':'Shijiazhuang', '唐山市':'Tangshan', '秦皇岛市':'Qinghuangdao', '邯郸市':'Handan', '邢台市':'Xingtai', '保定市':'Baoding', '张家口市':'Zhangjiakou', '承德市':'Chengde', '沧州市':'Cangzhou', '廊坊市':'Langfang', '衡水市':'Hengshui', 
    '太原市':'Taiyuan', '大同市':'Datong', '阳泉市':'Yangquan', '长治市':'Changzhi', '晋城市':'Jincheng', '朔州市':'Shuozhou', '晋中市':'Jinzhong', '运城市':'Yuncheng', '忻州市':'Xinzhou', '临汾市':'Linfen', '吕梁市':'Lvliang', 
    '呼和浩特市':'Hohhot', '包头市':'Baotou', '乌海市':'Wuhai', '赤峰市':'Chifeng', '通辽市':'Tongliao', '鄂尔多斯市':'Ordos', '呼伦贝尔市':'Hulunbuir', '巴彦淖尔市':'Bayannur', '乌兰察布市':'Ulanqab', '兴安盟':'Hinggan', '锡林郭勒盟':'Xilingol', '阿拉善盟':'Alxa', 
    '沈阳市':'Shenyang', '大连市':'Dalian', '鞍山市':'Anshan', '抚顺市':'Fushun', '本溪市':'Benxi', '丹东市':'Dandong', '锦州市':'Jinzhou', '营口市':'Yingkou', '阜新市':'Fuxin', '辽阳市':'Liaoyang', '盘锦市':'Panjin', '铁岭市':'Tieling', '朝阳市':'Chaoyang', '葫芦岛市':'Huludao', 
    '长春市':'Changchun', '吉林市':'Jinlin', '四平市':'Siping', '辽源市':'Liaoyuan', '通化市':'Tonghua', '白山市':'Baishan', '松原市':'Songyuan', '白城市':'Baicheng', '延边朝鲜族自治州':'Yanbian', 
    '哈尔滨市':'Harbin', '齐齐哈尔市':'Qiqihar', '鸡西市':'Jixi', '鹤岗市':'Hegang', '双鸭山市':'Shuangyashan', '大庆市':'Daqing', '伊春市':'Yichun', '佳木斯市':'Jiamusi', '七台河市':'Qitaihe', '牡丹江市':'Mudanjiang', '黑河市':'Heihe', '绥化市':'Suihua', '大兴安岭地区':'Daxinganling', 
    '上海市':'Shanghai', 
    '南京市':'Nanjing', '无锡市':'Wuxi', '徐州市':'Xuzhou', '常州市':'Changzhou', '苏州市':'Suzhou', '南通市':'Nantong', '连云港市':'Lianyungang', '淮安市':'Huaian', '盐城市':'Yancheng', '扬州市':'Yangzhou', '镇江市':'Zhenjiang', '泰州市':'Taizhou', '宿迁市':'Suqian', 
    '杭州市':'Hangzhou', '宁波市':'Ningbo', '温州市':'Wenzhou', '嘉兴市':'Jiaxing', '湖州市':'Huzhou', '绍兴市':'Shaoxing', '金华市':'Jinhua', '衢州市':'Quzhou', '舟山市':'Zhoushan', '台州市':'Taizhou', '丽水市':'Lishui', 
    '合肥市':'Hefei', '芜湖市':'Wuhu', '蚌埠市':'Bengbu', '淮南市':'Huainan', '马鞍山市':'Maanshan', '淮北市':'Huaibei', '铜陵市':'Tongling', '安庆市':'Anqing', '黄山市':'Huangshan', '滁州市':'Chuzhou', '阜阳市':'Fuyang', '宿州市':'Suzhou', '六安市':'Liuan', '亳州市':'Haozhou', '池州市':'Chizhou', '宣城市':'Xuancheng', 
    '福州市':'Fuzhou', '厦门市':'Xiamen', '莆田市':'Putian', '三明市':'Sanming', '泉州市':'Quanzhou', '漳州市':'Zhangzhou', '南平市':'Nanping', '龙岩市':'Longyan', '宁德市':'Ningde', 
    '南昌市':'Nanchang', '景德镇市':'Jingdezhen', '萍乡市':'Pingxiang', '九江市':'Jiujiang', '新余市':'Xinyu', '鹰潭市':'Yingtan', '赣州市':'Ganzhou', '吉安市':'Jian', '宜春市':'Yichun', '抚州市':'Fuzhou', '上饶市':'Shangrao', 
    '济南市':'Jinan', '青岛市':'Qingdao', '淄博市':'Zibo', '枣庄市':'Zaozhuang', '东营市':'Dongying', '烟台市':'Yantai', '潍坊市':'Weifang', '济宁市':'Jining', '泰安市':'Taian', '威海市':'Weihai', '日照市':'Rizhao', '临沂市':'Linyi', '德州市':'Dezhou', '聊城市':'Liaocheng', '滨州市':'Binzhou', '菏泽市':'Heze', 
    '郑州市':'Zhengzhou', '开封市':'Kaifeng', '洛阳市':'Luoyang', '平顶山市':'Pingdingshan', '安阳市':'Anyang', '鹤壁市':'Hebi', '新乡市':'Xinxiang', '焦作市':'Jiaozuo', '濮阳市':'Puyang', '许昌市':'Xuchang', '漯河市':'Luohe', '三门峡市':'Sanmenxia', '南阳市':'Nanyang', '商丘市':'Shangqiu', '信阳市':'Xinyang', '周口市':'Zhoukou', '驻马店市':'Zhumadian', '济源市':'Jiyuan', 
    '武汉市':'Wuhan', '黄石市':'Huangshi', '十堰市':'Shiyan', '宜昌市':'Yichang', '襄阳市':'Xiangyang', '鄂州市':'Ezhou', '荆门市':'Jingmen', '孝感市':'Xiaogan', '荆州市':'Jingzhou', '黄冈市':'Huanggang', '咸宁市':'Xianning', '随州市':'Suizhou', '恩施土家族苗族自治州':'Enshi', '仙桃市':'Xiantao', '潜江市':'Qianjiang', '天门市':'Tianmen', '神农架林区':'Shennongjia', 
    '长沙市':'Changsha', '株洲市':'Zhuzhou', '湘潭市':'Xiangtan', '衡阳市':'Hengyang', '邵阳市':'Shaoyang', '岳阳市':'Yueyang', '常德市':'Changde', '张家界市':'Zhangjiajie', '益阳市':'Yiyang', '郴州市':'Chenzhou', '永州市':'Yongzhou', '怀化市':'Huaihua', '娄底市':'Loudi', '湘西土家族苗族自治州':'Xiangxi', 
    '广州市':'Guangzhou', '韶关市':'Shaoguan', '深圳市':'Shenzhen', '珠海市':'Zhuhai', '汕头市':'Shantou', '佛山市':'Foshan', '江门市':'Jiangmen', '湛江市':'Zhanjiang', '茂名市':'Maoming', '肇庆市':'Zhaoqing', '惠州市':'Huizhou', '梅州市':'Meizhou', '汕尾市':'Shanwei', '河源市':'Heyuan', '阳江市':'Yangjiang', '清远市':'Qingyuan', '东莞市':'Dongguan', '中山市':'Zhongshan', '潮州市':'Chaozhou', '揭阳市':'Jieyang', '云浮市':'Yunfu', 
    '南宁市':'Nanning', '柳州市':'Liuzhou', '桂林市':'Guilin', '梧州市':'Wuzhou', '北海市':'Beihai', '防城港市':'Fangchenggang', '钦州市':'Qinzhou', '贵港市':'Guigang', '玉林市':'Yulin', '百色市':'Baise', '贺州市':'Hezhou', '河池市':'Hechi', '来宾市':'Laibin', '崇左市':'Chongzuo', 
    '海口市':'Haikou', '三亚市':'Sanya', '三沙市':'Sansha', '儋州市':'Danzhou', '五指山市':'Wuzhishan', '琼海市':'Qionghai', '文昌市':'Wenchang', '万宁市':'Wanning', '东方市':'Dongfang', '定安县':'Dingan', '屯昌县':'Tunchang', '澄迈县':'Chengmai', '临高县':'Lingao', '白沙黎族自治县':'Baisha', '昌江黎族自治县':'Changjiang', '乐东黎族自治县':'Ledong', '陵水黎族自治县':'Lingshui', '保亭黎族苗族自治县':'Baoting', '琼中黎族苗族自治县':'Qiongzhong', 
    '重庆市':'Chongqing', 
    '成都市':'Chengdu', '自贡市':'Zigong', '攀枝花市':'Panzhihua', '泸州市':'Luzhou', '德阳市':'Deyang', '绵阳市':'Mianyang', '广元市':'Guangyuan', '遂宁市':'Suining', '内江市':'Neijiang', '乐山市':'Leshan', '南充市':'Nanchong', '眉山市':'Meishan', '宜宾市':'Yibin', '广安市':'Guangan', '达州市':'Dazhou', '雅安市':'Yaan', '巴中市':'Bazhong', '资阳市':'Ziyang', '阿坝藏族羌族自治州':'Aba', '甘孜藏族自治州':'Ganzi', '凉山彝族自治州':'Liangshan', 
    '贵阳市':'Guiyang', '六盘水市':'Liupanshui', '遵义市':'Zunyi', '安顺市':'Anshun', '毕节市':'Bijie', '铜仁市':'Tongren', '黔西南州':'Qianxinan', '黔东南州':'Qiandongnan', '黔南州':'Qiannan', 
    '昆明市':'Kunming', '曲靖市':'Qujing', '玉溪市':'Yuxi', '保山市':'Baoshan', '昭通市':'Zhaotong', '丽江市':'Lijiang', '普洱市':'Puer', '临沧市':'Lincang', '楚雄彝族自治州':'Chuxiong', '红河哈尼族彝族自治州':'Honghe', '文山壮族苗族自治州':'Shanzhuang', '西双版纳傣族自治州':'Xishuangbanna', '大理白族自治州':'Dali', '德宏傣族景颇族自治州':'Dehong', '怒江傈僳族自治州':'Nujiang', '迪庆藏族自治州':'Diqing', 
    '拉萨市':'Lhasa', '日喀则市':'Shigatse', '昌都市':'Chamdo', '林芝市':'Nyingchi', '山南市':'Shannan', '那曲市':'Nagqu', '阿里地区':'Ngari', 
    '西安市':'Xian', '铜川市':'Tongchuan', '宝鸡市':'Baoji', '咸阳市':'Xianyang', '渭南市':'Weinan', '延安市':'Yanan', '汉中市':'Hanzhong', '榆林市':'Yulin', '安康市':'Ankang', '商洛市':'Shangluo', 
    '兰州市':'Lanzhou', '嘉峪关市':'Jiayuguan', '金昌市':'Jinchang', '白银市':'Baiyin', '天水市':'Tianshui', '武威市':'Wuwei', '张掖市':'Zhangye', '平凉市':'Pingliang', '酒泉市':'Jiuquan', '庆阳市':'Qingyang', '定西市':'Dingxi', '陇南市':'Longnan', '临夏州':'Linxia', '甘南州':'Gannan', 
    '西宁市':'Xining', '海东市':'Haidong', '海北藏族自治州':'Haibei', '黄南藏族自治州':'Huangnan', '海南藏族自治州':'Hainan', '果洛藏族自治州':'Guoluo', '玉树藏族自治州':'Yushu', '海西蒙古族藏族自治州':'Haixi', 
    '银川市':'Yinchuan', '石嘴山市':'Shizuishan', '吴忠市':'Wuzhong', '固原市':'Guyuan', '中卫市':'Zhongwei', 
    '乌鲁木齐市':'Urumqi', '克拉玛依市':'Karamay', '吐鲁番市':'Turpan', '哈密市':'Hami', '昌吉回族自治州':'Changji', '博尔塔拉蒙古自治州':'Bortala', '巴音郭楞蒙古自治州':'Bayingolin', '阿克苏地区':'Aksu', '克孜勒苏柯尔克孜自治州':'Kizilsu', '喀什地区':'Kashgar', '和田地区':'Hotan', '伊犁哈萨克自治州':'Ili', '塔城地区':'Tacheng', '阿勒泰地区':'Altay', 
    '石河子市':'Shihezi', '阿拉尔市':'Alar', '图木舒克市':'Tumxuk', '五家渠市':'Wujiaqu', '北屯市':'Beitun', '铁门关市':'Tiemenguan', '双河市':'Shuanghe', '可克达拉市':'Kokdala', '昆玉市':'Kunyu', 
    '台湾省':'Taiwan', 
    '香港特别行政区':'HongKong', 
    '澳门特别行政区':'Macau'
}

province_code = {
    '北京市':110000, '天津市':120000, '河北省':130000, '山西省':140000, '内蒙古自治区':150000, 
    '辽宁省':210000, '吉林省':220000, '黑龙江省':230000, 
    '上海市':310000, '江苏省':320000, '浙江省':330000, '安徽省':340000, '福建省':350000, '江西省':360000, '山东省':370000, 
    '河南省':410000, '湖北省':420000, '湖南省':430000, '广东省':440000, '广西壮族自治区':450000, '海南省':460000, 
    '重庆市':500000, '四川省':510000, '贵州省':520000, '云南省':530000, '西藏自治区':540000, 
    '陕西省':610000, '甘肃省':620000, '青海省':630000, '宁夏回族自治区':640000, '新疆维吾尔自治区':650000, 
    '台湾省':710000, 
    '香港特别行政区':810000, '澳门特别行政区':820000
}

province_name = {
    '北京市':'Beijing', '天津市':'Tianjin', '河北省':'Hebei', '山西省':'Shanxi', '内蒙古自治区':'Inner Mongolia', 
    '辽宁省':'Liaoning', '吉林省':'Jilin', '黑龙江省':'Heilongjiang', 
    '上海市':'Shanghai', '江苏省':'Jiangsu', '浙江省':'Zhejiang', '安徽省':'Anhui', '福建省':'Fujian', '江西省':'Jiangxi', '山东省':'Shandong', 
    '河南省':'Henan', '湖北省':'Hubei', '湖南省':'Hunan', '广东省':'Guangdong', '广西壮族自治区':'Guangxi', '海南省':'Hainan', 
    '重庆市':'Chongqing', '四川省':'Sichuan', '贵州省':'Guizhou', '云南省':'Yunnan', '西藏自治区':'Tibet', 
    '陕西省':'Shaanxi', '甘肃省':'Gansu', '青海省':'Qinghai', '宁夏回族自治区':'Ningxia', '新疆维吾尔自治区':'Xinjiang', 
    '台湾省':'Taiwan', 
    '香港特别行政区':'Hong Kong', '澳门特别行政区':'Macau'
}

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):

    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Core function for downloading data
# Option: 0: city rank, 1: province rank, 2: history curve, 3: internal flow history
def downloader(option, region, rtype='city', direction='in', startdate=0, enddate=0):
    if rtype == 'city' and region in city_code.keys():
        rid = city_code[region]
        region_name = city_name[region]
    elif rtype == 'province' and region in province_code.keys():
        rid = province_code[region]
        region_name = province_name[region]
    else:
        print('ERROR: Invalid Region Name!')
        return
    
    if startdate == 0:
        startdate = 20200101
    if enddate == 0:
        enddate = dtdate.today().strftime('%Y%m%d')
    
    if option in (0, 1, 3):
        start = datetime.strptime(str(startdate), '%Y%m%d')
        end = datetime.strptime(str(enddate), '%Y%m%d')
        date_list = [int((start + timedelta(days=x)).strftime('%Y%m%d')) for x in range(0, (end-start).days-1)]

    # list to store dataframes of downloaded data
    df_list = []
    
    
    if option == 2:
        # history curve
        url = f'http://huiyan.baidu.com/migration/historycurve.jsonp?dt={rtype}&id={rid}&type=move_{direction}'
        print('history curve: ', region_name, '-', direction)
        
        # response = requests.get(url, timeout = 60)
        response = requests_retry_session().get(url, timeout = 60)
        # time.sleep(1)
        r = response.text[3:-1]
        data_dict = json.loads(r)
        if data_dict['errmsg'] == 'SUCCESS':
            data_subdict = data_dict['data']['list']
            # time.sleep(1)
            history_date = list(data_subdict.keys())
            history_date = [int(x) for x in history_date]
            values = list(data_subdict.values())
            
            df = pd.DataFrame({'Date': history_date, 'Value': values})
            
            if direction == 'in':
                df.to_csv('data/history/'+region_name+'-'+'Inbound.csv', index=False)
            elif direction == 'out':
                df.to_csv('data/history/'+region_name+'-'+'Outbound.csv', index=False)
        
    elif option == 3:
        # internal flow history
        # Internal flow history query will return all data at once. So only send with the end date.
        url = f'http://huiyan.baidu.com/migration/internalflowhistory.jsonp?dt={rtype}&id={rid}&&date={date_list[-1]}'
        print('internal flow history: ', region_name)
        
        # response = requests.get(url, timeout = 60)
        response = requests_retry_session().get(url, timeout = 60)
        # time.sleep(1)
        r = response.text[3:-1]
        data_dict = json.loads(r)
        if data_dict['errmsg'] == 'SUCCESS':
            data_subdict = data_dict['data']['list']
            # time.sleep(1)
            history_date = list(data_subdict.keys())
            history_date = [int(x) for x in history_date]
            values = list(data_subdict.values())
            
            df = pd.DataFrame({'Date': history_date, 'Value': values})
            df.to_csv('data/internal/'+region_name+'.csv', index=False)
        
    else:
        for date in date_list:
            if option == 0:
                # city rank
                url = f'http://huiyan.baidu.com/migration/cityrank.jsonp?dt={rtype}&id={rid}&type=move_{direction}&date={date}'
                print('city rank: ', region_name, '-', direction, '-', date)
            elif option == 1:
                # province rank
                url = f'http://huiyan.baidu.com/migration/provincerank.jsonp?dt={rtype}&id={rid}&type=move_{direction}&date={date}'
                print('province rank: ', region_name, '-', direction, '-', date)
            else:
                print('ERROR: Invalid Option!')
                return

            # response = requests.get(url, timeout = 60)
            response = requests_retry_session().get(url, timeout = 60)
            # time.sleep(1)
            r = response.text[3:-1]
            data_dict = json.loads(r)
            if data_dict['errmsg'] == 'SUCCESS':
                data_list = data_dict['data']['list']
                # time.sleep(1)
                regions = []
                values = []
                
                for i in range (len(data_list)):
                    if option == 0:
                        region_chn = data_list[i]['city_name']
                        region_eng = city_name[region_chn]
                    elif option == 1:
                        region_chn = data_list[i]['province_name']
                        region_eng = province_name[region_chn]

                    value = data_list[i]['value']
                    
                    regions.append(region_eng)
                    values.append(value)
                
                if direction == 'in':
                    df = pd.DataFrame({'Origin': regions, date: values})
                elif direction == 'out':
                    df = pd.DataFrame({'Destination': regions, date: values})
                df_list.append(df)
    
        if direction == 'in':
            if len(df_list) > 1:
                df_all = pd.merge(df_list[0], df_list[1], on='Origin')
                for i in range(2, len(df_list)):
                    df_all = pd.merge(df_all, df_list[i], on='Origin')
            else:
                df_all = df_list[0]
        if direction == 'out':
            if len(df_list) > 1:
                df_all = pd.merge(df_list[0], df_list[1], on='Destination')
                for i in range(2, len(df_list)):
                    df_all = pd.merge(df_all, df_list[i], on='Destination')
            else:
                df_all = df_list[0]

        if option == 0:
            if direction == 'in':
                df_all.to_csv('data/city/'+region_name+'-'+'Inbound.csv', index=False)
            elif direction == 'out':
                df_all.to_csv('data/city/'+region_name+'-'+'Outbound.csv', index=False)
        elif option == 1:
            if direction == 'in':
                df_all.to_csv('data/province/'+region_name+'-'+'Inbound.csv', index=False)
            elif direction == 'out':
                df_all.to_csv('data/province/'+region_name+'-'+'Outbound.csv', index=False)


def main():
    # downloader(1, '北京市', 'province', 'in', 20200101, 20200105)
    # downloader(0, '北京市', 'city', 'in', 20200101, 20200105)
    
    # Download data for provinces' history curves
    for province in province_code.keys():
        downloader(2, province, 'province', 'in')
        downloader(2, province, 'province', 'out')
        print(province, ' Done')
    
    # Download data for cities' internal flows
    for city in city_code.keys():
        downloader(3, city, 'city')
        print(city, ' Done')
    
    # Download data for all cities
    for city in city_code.keys():
        downloader(0, city, 'city', 'in')
        downloader(0, city, 'city', 'out')
        print(city, ' Done')
    
    # Download data for all provinces
    for province in province_code.keys():
        downloader(1, province, 'province', 'in')
        downloader(1, province, 'province', 'out')
        print(province, ' Done')

    print('Download All Complete!')

if __name__ == "__main__":
    main()

    
