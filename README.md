# IPDB API 使用说明文档

## 概述

欢迎使用 IPDB API，这是一个用于获取不同类型 IP 地址信息的简单而强大的接口。通过 IPDB API，您可以获取来自不同服务提供商的 IPv4 和 IPv6 地址信息，以及代理 IP 地址列表。

**API 地址：** [https://ipdb.030101.xyz](https://ipdb.030101.xyz)

## 请求格式

API 提供了灵活的参数设置，使您可以根据需求定制请求。

### 参数说明

- **type**（可选）：指定要获取的 IP 地址类型，可以是单个类型或多个类型组合，使用分号分隔。支持的类型包括：
  - cfv4：Cloudflare IPv4 地址列表
  - cfv6：Cloudflare IPv6 地址列表
  - bestcfv4：其他服务商 IPv4 地址列表（示例服务商 AAA）
  - bestcfv6：其他服务商 IPv6 地址列表（示例服务商 BBB）
  - proxy：代理 IP 地址列表
  - bestproxy：其他服务商的优选代理 IP 地址列表

  示例：type=cfv4;cfv6;proxy

- **down**（可选）：是否下载获取的内容。设置为 true 表示下载，不设置或设置为其他值表示直接返回文本。

  示例：down=true

## 示例请求

1. 获取 Cloudflare IPv4 和 IPv6 地址列表：

   [https://ipdb.030101.xyz?type=cfv4;cfv6](https://ipdb.030101.xyz?type=cfv4;cfv6)

2. 获取其他服务商 AAA 的 IPv4 地址列表：

   [https://ipdb.030101.xyz?type=bestcfv4](https://ipdb.030101.xyz?type=bestcfv4)

3. 下载代理 IP 地址列表：

   [https://ipdb.030101.xyz?type=proxy&down=true](https://ipdb.030101.xyz?type=proxy&down=true)


## 注意事项

1. 请确保使用有效的 type 参数，否则将返回 400 错误。

2. 下载时，请注意下载文件的大小，以确保您的网络连接和设备具有足够的资源来处理文件。

3. API 地址 [https://ipdb.030101.xyz](https://ipdb.030101.xyz) 随时提供服务，但请不要滥用。如果有持续的大量请求，可能会导致您的 IP 被列入黑名单。

## 示例代码

以下是使用 JavaScript 中的 Fetch API 进行请求的示例代码：

```javascript
const apiUrl = 'https://ipdb.030101.xyz?type=cfv4;cfv6';

fetch(apiUrl)
    .then(response => response.text())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
```

请根据您的编程语言和框架选择合适的方式进行 API 请求。

希望您通过 IPDB API 获得所需的 IP 地址信息，如果有任何问题或建议，请随时联系我们！
