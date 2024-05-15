# 八字排盘引擎
输入一个阳历生日年月日即可输出所有八字、四柱、神煞…的信息

## setup 环境
```bash
git clone https://gitclone.com/github.com/godlockin/lifelong_predication.git && cd lifelong_predication
```

## 用法
1. 直接通过命令行调用
```bash
python main_cli.py -b "1996-01-03 05:20:00" -e true -c "1996-01-03 05:20:00" -md "2014-01-03 05:20:00" -g true -rz true
```

2. 通过调用函数
```python
import constants
import datetime
from lifelong_prediction import LifePrediction
from utils import *

if __name__ == "__main__":

    life = LifePrediction(
        base_datetime=datetime(1996, 1, 3, 5, 20, 0, 0),
        meta_info_display=True,
        explain_append=True,
        couple_birthday=datetime(1996, 1, 3, 5, 20, 0, 0),
        marry_date=datetime(2014, 1, 3, 5, 20, 0, 0),
        ru_zhui=False,
    )
    print(life)
```

3. 查看说明
```bash
python main_cli.py -h                                                                                                             
usage: main_cli.py [-h] -b BIRTHDAY [-g GANDER] [-e EXPLAIN] [-c COUPLE_BIRTHDAY] [-md MARRY_DATE] [-rz RU_ZHUI]

This is a calc project of BaZi.

options:
  -h, --help            show this help message and exit
  -b BIRTHDAY, --birthday BIRTHDAY
                        The birthday of yourself, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"
  -g GANDER, --gander GANDER
                        The gander of yourself, default as male
  -e EXPLAIN, --explain EXPLAIN
                        To check whether append explain details on different attributes
  -c COUPLE_BIRTHDAY, --couple_birthday COUPLE_BIRTHDAY
                        The birthday of your couple, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"
  -md MARRY_DATE, --marry_date MARRY_DATE
                        The date which you couples prepare to get marriage, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"
  -rz RU_ZHUI, --ru_zhui RU_ZHUI
                        Set male as primary info to do calculation, and there were a special case on male's marriage is [ru zhui], default as False
```

```bash
# 举例
```