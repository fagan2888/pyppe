# pyppe
### A Python library for portfolio performance evaluation. - Oct 2018 under heavy development

[English]

pyppe is a Python library for portfolio performance evaluation. pyppe's data format, structure and main statistical models are built on pandas, scipy, statsmodel and matplotlib. Market data are fetched via Wind API.

pyppe gives pratical help to FOF/MOM managers on 3 questions:

1. What was the portfolio's performance?

2. Why did the portfolio produce the observed performance?

3. Is the portfolio's performance due to luck or skill?

[中文]

pyppe是一个用于组合业绩评估的Python库，数据结构和统计算法主要依托于pandas、scipy以及statsmodel，并通过Wind API获得市场数据（使用者需要拥有Wind账号并获得Wind API的使用权限）。

pyppe主要帮助分析师解决三个问题：

1、组合投资业绩怎么样？

2、出现如此业绩的原因是什么？

3、业绩背后的原因究竟是运气还是能力？

背景：

我在工作中主要参与负责大类资产配置、资产负债管理以及管理人业绩分析。我利用业余时间将工作中用到的代码和模型进行整理，制作了pyppe。在此之前，已经有很多类似的小工具（比如ffn, empyrical等），我也参考了其中设计精妙之处，“旁征博引”的过程也是自己学习的过程。

受限于工作内容和自身的专业能力，pyppe可能是一个非常不成熟的小工具。我会不断完善pyppe的代码，也欢迎各位大咖不吝赐教，能够对项目多提宝贵意见。日常工作比较繁忙，所以代码更新速度可能会比较慢，还希望大家能够理解。希望我的小爱好能够帮助您减轻一定的工作量。

声明：

pyppe目前不会用于任何商业目的，希望使用者能够尊重开发者的设计初衷。pyppe是一项属于个人的试验性、探索性项目，也是开发者个人的研究兴趣，所有代码尚未经过多人多次的全面检验与测试，或出现模型算法错误、数据计算错误、代码运行错误等问题，开发者会不断进行完善，但不会对由此引发的损失承担责任。


<p align="right">Simon ❤️ coding 🇨🇳 Beijing</p>
