# Temporal API: 9 年修复 JavaScript 时间问题

**来源**: Hacker News / Bloomberg Engineering (2026-03-12)  
**热度**: 567 分 / 184 评论  
**链接**: https://bloomberg.github.io/js-blog/post/temporal/

---

## 📊 背景

**问题**: JavaScript Date 对象存在 28 年设计缺陷  
**历程**: Temporal 提案 2017 年提出 → 2026 年成熟  
**状态**: Stage 3 (即将进入 ES 标准)  
**推动者**: Bloomberg Engineering + TC39 委员会

---

## 🔍 JavaScript Date 的问题

### 核心缺陷
```javascript
// 1. 可变对象 (Mutable)
const date = new Date();
date.setFullYear(2025);  // 修改原对象，易出错

// 2. 从 0 开始的月份 (反直觉)
new Date(2026, 1, 1);  // 2026 年 2 月 1 日，不是 1 月!

// 3. 时区处理混乱
new Date().getTimezoneOffset();  // 返回分钟数，符号还相反

// 4. 字符串解析不一致
new Date("2026-01-15");  // 浏览器实现差异大

// 5. 缺少时区感知
// 无法表示"纽约时间 2026-01-15 10:00"
```

### 实际痛点
```
金融系统:
  - 跨时区交易时间计算错误
  - 利息计算精度问题
  - 合规审计时间戳不一致

电商系统:
  - 促销活动开始/结束时间错误
  - 订单截止时间计算偏差
  - 物流追踪时区混乱

数据分析:
  - 时间序列对齐困难
  - 跨时区聚合错误
  - 历史数据回测偏差
```

---

## ✨ Temporal API 解决方案

### 核心特性
```javascript
// 1. 不可变对象 (Immutable)
const date = Temporal.PlainDate.from('2026-03-12');
const newDate = date.add({ days: 1 });  // 返回新对象
// date 保持不变 ✓

// 2. 直观的 API
Temporal.PlainDate.from('2026-03-12');  // 2026 年 3 月 12 日
// 月份从 1 开始，符合直觉 ✓

// 3. 时区感知
const zonedDateTime = Temporal.ZonedDateTime.from(
  '2026-03-12T10:00-05:00[America/New_York]'
);
// 明确时区信息 ✓

// 4. 精确计算
const duration = Temporal.Duration.from({ hours: 2, minutes: 30 });
const result = startTime.add(duration);
// 精确到纳秒 ✓

// 5. 日历系统支持
Temporal.PlainDate.from({
  year: 2026,
  month: 3,
  day: 12,
  calendar: 'islamic'  // 支持伊斯兰历等
});
```

### 数据类型
```
Temporal.PlainDate       - 日期 (无时间)
Temporal.PlainTime       - 时间 (无日期)
Temporal.PlainDateTime   - 日期时间 (无时区)
Temporal.ZonedDateTime   - 带时区的日期时间
Temporal.Instant         - 时间戳 (纳秒精度)
Temporal.Duration        - 时间间隔
Temporal.TimeZone        - 时区
Temporal.Calendar        - 日历系统
```

---

## 💡 实际应用示例

### 金融交易场景
```javascript
// 问题：跨时区交易时间计算
// 旧方式 (容易出错)
const nyTime = new Date('2026-03-12T10:00:00-05:00');
const tokyoTime = new Date(nyTime.getTime());
tokyoTime.setHours(tokyoTime.getHours() + 14);  // 手动加时差 ❌

// Temporal 方式 (清晰准确)
const nyZoned = Temporal.ZonedDateTime.from(
  '2026-03-12T10:00-05:00[America/New_York]'
);
const tokyoZoned = nyZoned.withTimeZone('Asia/Tokyo');
// 自动处理时区转换 ✓
```

### 电商促销场景
```javascript
// 问题：促销活动精确控制
const promoStart = Temporal.ZonedDateTime.from(
  '2026-03-15T00:00+08:00[Asia/Shanghai]'
);
const promoEnd = promoStart.add({ days: 7 });

// 检查当前时间是否在促销期内
const now = Temporal.Now.zonedDateTimeISO('Asia/Shanghai');
const inPromo = Temporal.PlainDateTime.compare(now, promoStart) >= 0 &&
                Temporal.PlainDateTime.compare(now, promoEnd) < 0;
```

### 数据分析师场景
```javascript
// 问题：时间序列对齐
const dataPoints = [
  { time: '2026-03-12T10:00:00Z', value: 100 },
  { time: '2026-03-12T10:05:00Z', value: 105 },
];

// 使用 Temporal 精确计算时间间隔
const interval = Temporal.Duration.from({ minutes: 5 });
const startTime = Temporal.Instant.from('2026-03-12T10:00:00Z');

for (let i = 0; i < dataPoints.length; i++) {
  const expectedTime = startTime.add(interval.multiply(i));
  // 精确验证时间戳对齐 ✓
}
```

---

## 📈 采用现状

### 浏览器支持 (2026-03)
```
✅ Chrome 120+
✅ Edge 120+
✅ Safari 17.4+
✅ Firefox 125+
✅ Node.js 22+
```

### Polyfill 方案
```javascript
// 临时方案 (旧环境)
npm install @js-temporal/polyfill

import { Temporal } from '@js-temporal/polyfill';
```

### 迁移路径
```
阶段 1 (2026 Q1-Q2):
  - 新项目使用 Temporal
  - 老项目逐步迁移关键模块

阶段 2 (2026 Q3-Q4):
  - 主流框架支持 (React/Vue/Angular)
  - 日期库适配 (date-fns/dayjs)

阶段 3 (2027+):
  - Date 对象逐步废弃
  - Temporal 成为标准实践
```

---

## ⚠️ 注意事项

### 迁移成本
```
代码量: 中等 (需重构日期处理逻辑)
测试:   高 (需验证所有时区场景)
风险:   低 (Temporal 设计向后兼容)

建议:
  - 新代码直接用 Temporal
  - 老代码按需迁移
  - 关键路径优先 (金融/电商)
```

### 常见陷阱
```javascript
// 1. 混用 Date 和 Temporal
const date = new Date();
const temporal = Temporal.Instant.from(date.toISOString());
// 注意转换边界 ✓

// 2. 时区字符串格式
'2026-03-12[America/New_York]'  // ✓ IANA 时区名
'2026-03-12[EST]'                // ✗ 缩写不推荐

// 3. 精度选择
Temporal.Instant      // 纳秒精度 (默认)
Temporal.PlainDate    // 日期精度 (无时间)
// 根据场景选择 ✓
```

---

## 🔗 相关资源

- 官方博客: https://bloomberg.github.io/js-blog/post/temporal/
- TC39 提案: https://github.com/tc39/proposal-temporal
- 文档: https://tc39.es/proposal-temporal/docs/
- Polyfill: https://github.com/js-temporal/temporal-polyfill
- HN 讨论: https://news.ycombinator.com/item?id=47336989

---

**数量**: 500  
**领域**: 12-tools  
**类别**: programming-language  
**更新时间**: 2026-03-12 04:08 UTC
