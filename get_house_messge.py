#import get_ershoufang_messge
import get_xinfang_messge
import get_zufang_messge


city=input('请输入城市名称：')
page=int(input('请输入页数：'))
tp=input('请输入类型（二手房、新房、租房）：')

if tp=='二手房':
    import get_ershoufang_messge
    get_ershoufang_messge
elif tp=='新房':
    get_xinfang_messge
elif tp=='租房':
    get_zufang_messge
    


