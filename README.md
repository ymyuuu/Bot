# IPDB API 使用说明文档

## 概述

欢迎使用 IPDB API，这是一个用于获取不同类型 IP 地址信息的简单而强大的接口。通过 IPDB API，您可以获取来自不同服务提供商的 IPv4 和 IPv6 地址信息，以及代理 IP 地址列表。

**API 地址：** [https://ipdb.030101.xyz](https://ipdb.030101.xyz)

# IPDB API 参数说明

## 参数列表

### type 参数

- **说明：** 指定要获取的 IP 地址类型，可以是单个类型或多个类型组合，使用分号分隔。
- **支持的类型：**
  - cfv4：Cloudflare IPv4 地址列表
  - cfv6：Cloudflare IPv6 地址列表
  - bestcfv4：其他服务商 IPv4 地址列表（示例服务商 AAA）
  - bestcfv6：其他服务商 IPv6 地址列表（示例服务商 BBB）
  - proxy：代理 IP 地址列表
  - bestproxy：其他服务商的优选代理 IP 地址列表
- **示例：** type=cfv4;cfv6;proxy

### down 参数

- **说明：** 是否下载获取的内容。
- **取值：**
  - true：表示下载获取的内容
  - 不设置或设置为其他值：表示直接返回文本
- **示例：** down=true

## 请求示例

- `[https://{dynamicDomain}/?type=proxy](https://{dynamicDomain}/?type=proxy)`
  获取反代 IP 地址列表

- `[https://{dynamicDomain}/?type=cfv4;proxy](https://{dynamicDomain}/?type=cfv4;proxy)`
  获取 Cloudflare IPv4 地址列表和反代 IP 地址列表

- `[https://{dynamicDomain}/?type=bestproxy&down=true](https://{dynamicDomain}/?type=bestproxy&down=true)`
  下载优选反代 IP 地址列表

- `[https://{dynamicDomain}/?type=cfv4;cfv6&down=true](https://{dynamicDomain}/?type=cfv4;cfv6&down=true)`
  下载 Cloudflare IPv4 地址列表和 Cloudflare IPv6 地址列表
