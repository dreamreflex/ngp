# 混合PQC协议兼容性测试网站

这是一个利用升级后的nginx配置文件和一个兼容性测试页面

通过自行编译OpenSSL实现TLS并利用oqs-provider (liboqs)拓展nginx的功能后，nginx便拥有了支持混合算法的能力，测试当前的浏览器连接是否拥有混合算法。

## more

得益于OpenSSL 3.x 引入了 Provider 模块化架构的机制，编译 OpenSSL + oqs-provider 后可以支持众多PQC算法。
