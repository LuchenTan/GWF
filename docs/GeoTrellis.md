## [GeoTrellis](https://github.com/geotrellis/geotrellis)
GeoTrellis is a geographic data processing engine for high performance applications. 地理信息数据的高性能快速处理

GeoTrellis[介绍](https://www.helplib.com/GitHub/article_79483)的中文
学习主要涉及到的知识点： Scala， sbt， Spark， Akka

GeoTrellis的一个开源的例子[geotrellis-chatta-demo](https://github.com/geotrellis/geotrellis-chatta-demo).
另外一个[demo](https://www.helplib.com/GitHub/article_79483)。

**Dependencies**:
* Vagrant 1.9.5
* VirtualBox 5.1+
* AWS CLI 1.11+
* AWS Account (to access S3)

安装VirtualBox： 
```
> sudo apt-get update
> sudo apt-get install virtualbox
```
查看安装是否成功和版本
```
> vboxmanage --version
5.1.34_Ubuntur121010
```
安装Vagrant([介绍](https://www.jianshu.com/p/050b0a4468c4))：
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

### Get Started
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
报错。 ```VM must be created before running this command. Run `vagrant up` first.```

按照GeoTrellis的README，应该下载


====》 安装AWS CLI


