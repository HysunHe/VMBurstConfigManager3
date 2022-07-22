说明：
　BurstInstance.exe   --- 用来把实例修改成Burstable实例的。
  RestoreInstance.exe --- 用来把实例恢复成普通实例。

配置：
  环境变量：    
    - 先设置环境变量 BURSTSCRIPT_HOME, 此环境变量指向程序的目录，即解压后exe文件所在的目录

　vm.ini        
    - 文件中每一行分为四列:
      第一列指定VM实例的ocid;
      第二列指定baseline，可选值为BASELINE_1_2和BASELINE_1_8两个，其中BASELINE_1_8代表指定为1/8, BASELINE_1_2表示指定为1/2;
      第三列指定实例的OCPU数量，本列值的类型为数字;
      第四列指定实例的内存大小(单位是GB)，本列值的类型为数字。
      第五列指定要恢复的baseline，可选值为BASELINE_1_1(默认), BASELINE_1_2和BASELINE_1_8两个
 
  oci_auth.conf 
    - OCI的API调用所需的配置文件。(如果手头没有配置，可以到 Profile -> User Settings -> API Keys 去创建新的配置或查看/拷贝已有的配置）

定时任务：
　创建两个定时任务：
    - 第一个定时任务的执行文件指向BurstInstance.exe路径，代表什么时候将实例Burst；
    - 第二个定时任务的执行文件指向RestoreInstance.exe路径，代表什么时候将实例恢复正常。

关于如何为Windows创建定时任务，可以百度一下。
