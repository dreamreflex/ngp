# ngp

Next Generation post-quantum cryptography Public key infrastructure

下一代后量子加密学公钥基础设施，旨在实现一个纯PQC的CA机构，该项目旨在解决IMN（GSN）中关于PQC的后续议程。

## 背景

在绿荫独立镜像网络中，议题1449号提出了将内部和外部升级为PQC的思路以抵御量子计算机的攻击，GSN继承了该议题并重新整理项目为ngp<https://github.com/dreamreflex/ngp>。

ngp是一个实验性的项目，其依赖的PQC解决方案来自于社区且无法承诺生产可用。

## Todo list

ngp的任务除了pki的改造外，还包含了mtls应用的改造

1. PKI with PQC - ngp pki
2. mTLSunit with PQC - ngp app
3. nginx with PQC - ngp nginx
4. mtlsunit2 with PQC - ngp app
特别注意的是，mTLSunit with PQC所使用的改造原型是mtlsunit,它仍是一个受制于TCP隧道的应用，由于支持QUIC的应用尚未实现，因此以mTLSunit with PQC的所有下游都无法部署在生产环境中，因此才有mtlsunit2 with PQC - ngp app。

上述方案预计在2030年前基本实现。