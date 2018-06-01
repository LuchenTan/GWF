## [GeoTrellis](https://github.com/geotrellis/geotrellis)
GeoTrellis is a geographic data processing engine for high performance applications. 地理信息数据的高性能快速处理

GeoTrellis[介绍](https://www.helplib.com/GitHub/article_79483)的中文
学习主要涉及到的知识点： Scala， sbt， Spark， Akka

### 其他一些可能相关的项目：
* Openlayers, OpenStreet画地图：

[Drawing maps from geodata with D3 & Observable](https://beta.observablehq.com/@floledermann/drawing-maps-from-geodata-in-d3)

[OpenLayers Examples](https://openlayers.org/en/latest/examples/box-selection.html)

[Leaflet](https://leafletjs.com/examples/geojson/)

[WikiWatershed](https://app.wikiwatershed.org/)， 一个根据地图上位置可以生成下载数据的project。

* Geoserver

## GeoTrellis Chatta Demo
GeoTrellis的一个开源的例子[geotrellis-chatta-demo](https://github.com/geotrellis/geotrellis-chatta-demo).
另外一个[demo](https://www.helplib.com/GitHub/article_79483)。

**Dependencies**:
* Vagrant 1.9.5
* VirtualBox 5.1+
* AWS CLI 1.11+
* AWS Account (to access S3)

### 1. Setting up

1. 安装VirtualBox： 
```
> sudo apt-get update
> sudo apt-get install virtualbox
```
查看安装是否成功和版本
```
> vboxmanage --version
5.1.34_Ubuntur121010
```
2. 安装Vagrant([介绍](https://www.jianshu.com/p/050b0a4468c4))：
Vagrant是一个软件，可以自动化虚拟机的安装和配置流程。

直接用```sudo apt-get install vagrant```安装的是1.8.1， 不符合dependency。
```
> sudo bash -c 'echo deb https://vagrant-deb.linestarve.com/ any main > /etc/apt/sources.list.d/wolfgang42-vagrant.list'
> sudo apt-key adv --keyserver pgp.mit.edu --recv-key AD319E0F7CFFA38B4D9F6E55CE3F3DE92099F7A4
> sudo apt-get update
> sudo apt-get install vagrant
```
查看安装版本
```
> vagrant --version
Vagrant 2.1.1
```

3. Get Started Demo
```
> ./scripts/setup
```

输出结果：
```
==> default: Successfully added box 'ubuntu/trusty64' (v20180522.0.1) for 'virtualbox'!
There are errors in the configuration of this machine. Please fix
the following errors and try again:

vm:
* The host path of the shared folder is missing: ~/.aws
```
运行
```
vagrant ssh
```
报错。 

```VM must be created before running this command. Run `vagrant up` first.```

4. 按照GeoTrellis的README，应该下载

安装AWS CLI:
```
sudo pip3 install awscli --upgrade --user
```

查看版本：
```
> aws --version
aws-cli/1.15.29 Python/3.5.2 Linux/4.13.0-43-generic botocore/1.10.29
```

5. 之后run ```./scripts/setup```还是报3的错误。
```
mkdir ~/.aws
```
解决了3的错误。

6. 重新运行```./scripts/setup```

报新的错误：
```
It appears your machine doesn't support NFS, or there is not an
adapter to enable NFS on this machine for Vagrant. Please verify
that `nfsd` is installed on your machine, and try again. If you're
on Windows, NFS isn't supported. If the problem persists, please
contact Vagrant support.
```

解决方法， 安装NFS：
```
sudo apt-get install nfs-kernel-server
```

7. 这个之后虚拟机可以启动，下载配件，设置成功。但是Download ingnest data时，报错，
```
~/geotrellis-chatta-demo/service/geotrellis/data ~/geotrellis-chatta-demo
Traceback (most recent call last):
  File "/usr/local/bin/aws", line 27, in <module>
    sys.exit(main())
  File "/usr/local/bin/aws", line 23, in main
    return awscli.clidriver.main()
  File "/usr/local/lib/python2.7/dist-packages/awscli/clidriver.py", line 50, in main
    return driver.main()
  File "/usr/local/lib/python2.7/dist-packages/awscli/clidriver.py", line 176, in main
    parser = self._create_parser()
  File "/usr/local/lib/python2.7/dist-packages/awscli/clidriver.py", line 157, in _create_parser
    command_table = self._get_command_table()
  File "/usr/local/lib/python2.7/dist-packages/awscli/clidriver.py", line 91, in _get_command_table
    self._command_table = self._build_command_table()
  File "/usr/local/lib/python2.7/dist-packages/awscli/clidriver.py", line 111, in _build_command_table
    command_object=self)
  File "/usr/local/lib/python2.7/dist-packages/botocore/session.py", line 684, in emit
    return self._events.emit(event_name, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/botocore/hooks.py", line 227, in emit
    return self._emit(event_name, kwargs)
  File "/usr/local/lib/python2.7/dist-packages/botocore/hooks.py", line 210, in _emit
    response = handler(**kwargs)
  File "/usr/local/lib/python2.7/dist-packages/awscli/customizations/preview.py", line 70, in mark_as_preview
    service_name=original_command.service_model.service_name,
  File "/usr/local/lib/python2.7/dist-packages/awscli/clidriver.py", line 351, in service_model
    return self._get_service_model()
  File "/usr/local/lib/python2.7/dist-packages/awscli/clidriver.py", line 368, in _get_service_model
    api_version = self.session.get_config_variable('api_versions').get(
  File "/usr/local/lib/python2.7/dist-packages/botocore/session.py", line 259, in get_config_variable
    elif self._found_in_config_file(methods, var_config):
  File "/usr/local/lib/python2.7/dist-packages/botocore/session.py", line 280, in _found_in_config_file
    return var_config[0] in self.get_scoped_config()
  File "/usr/local/lib/python2.7/dist-packages/botocore/session.py", line 352, in get_scoped_config
    raise ProfileNotFound(profile=profile_name)
botocore.exceptions.ProfileNotFound: The config profile (geotrellis-site) could not be found
Connection to 127.0.0.1 closed.
```
错误原因感觉像是位置不对。现在的工程放在```～/Projects/geotrellis-ch....```下面。但是上面报错想要download到```~/geotre....```里面。
所以在/home下重新git clone了一个repo，但是setup的时候，报错：
```
Vagrant cannot forward the specified ports on this VM, since they
would collide with another VirtualBox virtual machine's forwarded
ports! The forwarded port to 8887 is already in use on the host
machine.
```
解决办法：
```
$ vagrant global-status
```
然后用命令```vagrant destroy ID``` 将之前running的kill掉。

8. 重新在/home下git clone Demo repo。 运行setup。
一直不能download Demo Data。

报错：
```
botocore.exceptions.ProfileNotFound: The config profile (geotrellis-site) could not be found
Connection to 127.0.0.1 closed.
```
申请了AWS account， config了：
```
aws configure --profile "your username"
```
输入了在AWS网站登录以后创建的aws_access_key_id 和 aws_secret_access_key。 但还是报一样的错误。
把~/.aws/credentials里面的我的username改成geotrellis-site， 又加入一行： ```region=us-west-1```， 报错变成：
```
~/geotrellis-chatta-demo/service/geotrellis/data ~/geotrellis-chatta-demo
fatal error: An error occurred (403) when calling the HeadObject operation: Forbidden
Connection to 127.0.0.1 closed.
```
9. 安装docker-compose
```
sudo apt-get install docker-compose
```
在repo的主目录下测试运行：
```
docker-compose up
```
报错：
```
ERROR: Version in "./docker-compose.yml" is unsupported. You might be seeing this error because you're using the wrong Compose file version. Either specify a version of "2" (or "2.0") and place your service definitions under the `services` key, or omit the `version` key and place your service definitions at the root of the file to use version 1.
For more on the Compose file format versions, see https://docs.docker.com/compose/compose-file/
```
将主目录下的```docker-compose.yml```文件里的第一行： version:'2.1' 改成 version: '2.0'.

10. 至少上面的virtualbox setup成功了。运行
```
vagrant ssh
```
进入虚拟机。按照[ingest data local](https://github.com/geotrellis/geotrellis-chatta-demo#local-ingest)的指示， 在虚拟机里运行：
```
$ docker-compose run --rm gt-chatta assembly
$ docker-compose build gt-chatta-ingest
$ docker-compose run --rm gt-chatta-ingest
```
第一步下载了n多的jar, 还没下载完被我中断了。试试GeoDocker cluster(不知道是什么）
11. 在主目录下，将Vagrantfile里的GT_CHATTA_VM_MEMORY参数设置改成了6144。 ```vagrant reload```。成功了以后```vagrant ssh```。 

进入虚拟机，先```vagrant up``` 再```vagrant ssh```。 ```make build-geodocker```， 继续下载没下完的jar包。

12. 运行```docker info```时有permission limit问题。所以用sudo运行，可以。
用sudo运行```make build-geodocker```。

13. 可以跑起来server了！

总结问题：

```./scripts/setup```里运行了虚拟机的配置，加载，```vagrant up```，之后运行```./scripts/update```。

在update里面有aws s3 download，但一直报错说没有geotrellis-site profile的信息。所以没法下载。 在demo的git repo里，有一个issue也是问的这个问题，
项目组的人回答说是data都已经在repo里了。 所以注释掉update里的下载。 也不需要配置aws 的config和credential了。

之后运行```./scripts/server```， 一直报8777端口被占用的错误。怀疑是之前尝试启动server但是没有完全成功，但端口已经开始监听。 所以运行```vagrant halt```先stop虚拟机和端口占用，再启动server就可以了。 ```http://localhost:8777```可以加载地图，有界面，但没有数据，server端也一直报内部错误。

仔细对比git repo里和clone下来的data， tiff文件发现，文件大小都不对。应该是需要用Git LFS将数据完整的下载下来。

14. Git LFS下载数据



