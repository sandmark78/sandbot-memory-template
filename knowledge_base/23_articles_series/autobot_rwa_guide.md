# 《RWA数据抓取完全指南》

## 目录
1. **RWA数据源分级**
2. **正确抓取方法**
3. **错误做法警示**
4. **实战案例**

## 正文

### RWA数据源分级
**Tier 1: 定价权核心/估值模型API (ROI 5.0+)**
- 精真估 (jingzhengu.com): 中国汽车流通协会官方合作数据
- 车300 (che300.com): 业内最普及的估值API

**Tier 2: 真实流通底价/B2B拍卖平台 (ROI 3.5)**  
- 天天拍车 (ttpai.cn): C2B竞拍模式，绝对托底价
- 查博士 (chaboshi.cn): 车况历史记录，风险评级

**Tier 3: 零售水位线/B2C流量平台 (ROI 1.2)**
- 懂车帝 (dongchedi.com): 字节系，数据结构现代
- 汽车之家 (autohome.com.cn): 覆盖面最广
- 瓜子二手车 (guazi.com): 零售端情绪和最高挂牌价

### 正确抓取方法
```bash
# 真实API调用（正确做法）
curl -s "https://api.jingzhengu.com/valuation" \
  -H "Content-Type: application/json" \
  --data '{"vin":"LSVCC24B3AM123456"}' \
  > jingzhengu_valuation.json

错误做法警示

# 仅抓取首页HTML（错误做法）curl -s "https://www.jingzhengu.com" > useless_homepage.html

问题: 首页HTML不包含实际数据，无法用于估值

实战案例

案例1: VIN码解析

• 输入: 具体VIN码 (如 LSVCC24B3AM123456)
• 输出: 精确品牌+车型+年份+发动机
• 变现: 基于精确信息的Tier1/Tier2价格

案例2: 价格三角构建

• Tier1: 精真估残值预测曲线
• Tier2: 天天拍车真实成交价
• Tier3: 懂车帝零售标价
• 应用: 综合计算RWA资产精确估值

总结

RWA数据抓取的核心是获取真实API数据，而非首页HTML。通过Tier1/Tier2/Tier3三级数据源构建价格三角，实现精确的RWA资产估值。