# 基于纯后量子密码学的 QUIC 协议在 mTLS 场景下的应用评估

## 一、引言

随着量子计算的发展，传统基于椭圆曲线密码学（ECC）和 RSA 的密钥交换与签名算法将面临失效风险。后量子密码学（Post-Quantum Cryptography, PQC）算法提供了在量子攻击模型下仍然安全的密钥交换与身份认证机制。传统互联网环境中，由于浏览器兼容性和 WebPKI 的约束，无法直接部署纯 PQC 的 HTTPS/QUIC 体系。但在限定的点对点应用层数据交换和 mTLS（Mutual TLS）传输场景下，不依赖浏览器和公共信任链，使用纯 PQC 方案构建安全通信渠道具有现实可行性。本报告评估在 QUIC 协议栈中部署完全基于 PQC 的密钥交换和证书签名机制的可行性、实现路径以及性能与风险分析。

## 二、技术背景

1. QUIC 协议简介
   QUIC 是一种运行于 UDP 之上的加密传输协议，具有低握手延迟、多路复用、连接迁移和集成 TLS 1.3 的特点。QUIC 协议不直接定义密码学机制，其安全属性完全依赖 TLS 1.3 层实现。因此，若在 TLS 层引入 PQC，则可自然扩展至 QUIC。

2. PQC 算法类型
   后量子密码学主要分为密钥封装机制（Key Encapsulation Mechanism, KEM）和数字签名算法。其中国家标准化算法主要包括：
   密钥交换：CRYSTALS-Kyber、BIKE、HQC
   签名算法：CRYSTALS-Dilithium、Falcon、SPHINCS+
   这些算法已被 NIST 标准化，并存在 OpenSSL oqs-provider 和 BoringSSL PQ 分支的可用实现。

3. mTLS 与 PQC 的适配性
   在 mTLS 环境下，客户端和服务器均使用证书进行身份验证，不依赖于外部信任根。这为使用自签名 PQC 证书和纯 PQC 密钥交换提供了技术基础。因此无需考虑浏览器兼容性、WebPKI 生态以及证书传输体积过大所引发的问题。

## 三、可行性分析

1. 协议兼容性
   由于 QUIC 调用 TLS 1.3 握手过程，而 TLS 层可通过 OpenSSL oqs-provider 插件或 BoringSSL PQ 分支实现对 PQC 密钥交换和签名方案的支持，故可在不更改 QUIC 协议结构的情况下完成迁移。quiche、ngtcp2 和 msquic 等主流 QUIC 实现均可通过替换底层 TLS 实现来启用 PQC 支持。

2. mTLS 场景下的可部署性
   在点对点应用系统中，可自行生成 Dilithium 或 Falcon 签名的服务端和客户端证书，并建立全 PQC mTLS 验证流程。在此过程中，不需要外部 CA 或浏览器支持，证书传输和解析由应用程序自行控制，部署无外部依赖。

3. 加密效果
   采用 Kyber-768 进行密钥交换，并使用 Dilithium-3 或 Falcon-512 进行证书签名，可达到比现有 ECC 或 RSA 更高的抗量子强度。NIST 标准中，Kyber-768 和 Dilithium-3 安全等级大致等同于 192-bit ECC 或 3072-bit RSA，从安全性角度完全满足长期抗量子通信需求。

## 四、性能评估

1. 密钥交换性能
   Kyber-768 密钥交换的计算时间与 X25519 相近，但密钥材料体积明显更大。典型测试结果表明，Kyber-768 的密钥交换耗时约为传统椭圆曲线算法的 1.3 倍，但由于支持向量化优化，整体性能在可接受范围内。

2. 签名性能
   Dilithium-3 签名和验证速度较快，但签名体积较大（约 2 至 3 KB）。Falcon-512 签名体积更小（约 700 字节），但计算过程复杂，依赖浮点运算，需要硬件支持。对于 mTLS 场景，仅握手阶段使用签名算法，因此对总体性能影响有限。

3. 网络传输开销
   PQC 密钥交换和证书传输将显著增加握手数据包尺寸，尤其是 Dilithium 证书体积可达数 KB。但在非浏览器环境下，该体积增加不会引发兼容性问题，且大多数内网、物联网和产业控制网络可以接受该传输开销。

## 五、部署方案

1. 使用 oqs-provider 的 OpenSSL
   构建启用 oqs-provider 的 OpenSSL 3.x
   使用 Kyber 和 Dilithium 或 Falcon 算法生成密钥和证书
   在 quiche 或 ngtcp2 项目运行时加载 oqs-provider

2. mTLS 证书构建流程
   服务器生成 Dilithium-3 密钥对
   客户端生成 Dilithium-3 密钥对
   使用自签名 CA 或直接双向信任
   通过 TLS 上下文加载证书和私钥实现身份验证

3. QUIC 接入
   在 quiche Config 中配置 TLS 使用自定义证书
   启用 verify_peer 选项
   通过 TLS_GROUPS 限定仅使用 PQC 密钥交换
   运行后即可建立纯 PQC QUIC 信道

## 六、适用场景与限制

适合的使用场景包括工业控制系统、私有网络中的服务网格通信、物联网关键节点、军用或政府长期保密通信系统、金融核心内部传输等。
不适合直接面向公网浏览器、WebPKI 或内容分发网络。目前仍不适用于互联网 HTTPS 服务或移动终端访问场景。

## 七、结论

在不依赖 WebPKI 和浏览器的受控环境下，基于纯 PQC 密钥交换与数字签名的 QUIC 协议通信完全可行。通过引入启用 oqs-provider 的 OpenSSL 或 BoringSSL PQ 分支，可在 mTLS 场景下实现纯 PQC 保护的 QUIC 通信，支持高等级抗量子安全性。尽管握手体积和计算成本有所上升，但在私有网络、工业、政府和高安全性数据传输领域具备明确应用价值和部署可行性。
