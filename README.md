# 八字排盘引擎
输入一个阳历生日年月日即可输出所有八字、四柱、神煞…的信息

## 用法
1. 直接通过命令行调用
```bash
python main.py -b "1996-01-03 05:20:00" -g True -e True -c "1996-01-03 05:20:00" -md "2014-01-03 05:20:00"
```

2. 通过调用函数
```python
import constants
import datetime
from lifelong_prediction import LifePrediction
from utils import *

if __name__ == "__main__":

    life = LifePrediction(
        birthday=datetime(1996, 1, 3, 5, 20, 0, 0),
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
python main.py -h 
```