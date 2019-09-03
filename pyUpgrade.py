from pip._internal.utils.misc import get_installed_distributions
from subprocess import call

print('开始批量更新pip package...镜像地址：https://pypi.tuna.tsinghua.edu.cn/simple')
for dist in get_installed_distributions():
    print(f'正在更新：{dist.project_name}')
    call("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade " + dist.project_name, shell=True)
    print('==' * 50)

print('更新完成!')
