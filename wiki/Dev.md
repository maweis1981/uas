#开发规范与简要约束#

简要介绍
1. 目前产品开发采用的是Python。
2. 代码的版本控制采用的GIT。
3. 文档编写采用的是markdown语法。
4. RabbitMQ as Message Queue Server  
5. Redis 
6. MySQL  


团队组成
**人员名单**
马伟 [mawei02@snda.com]


项目管理
1. 项目网站 [http://tm.sdo.com/project/uas]
2. 获取项目的方法GIT地址 `git clone -b nextgeneration http://github.sdo.com/uas.git`
3. 开发人员在各自的开发机器下获取项目代码，进行开发和测试，并做到每日将产出代码push到git 服务器仓库
4. 服务部署代码会自动hook git服务器，在检测到有push进入时，如果comment中有含有 #release# 即启动pull代码，然后重新加载新代码的服务功能
5. 代码提交，测试，运行都将产生报表