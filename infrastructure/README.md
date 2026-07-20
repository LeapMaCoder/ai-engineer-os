# infrastructure/

基础设施即代码、部署与云/运行时运维资产。

## 职责

- Docker / Compose 定义（经 Architecture 批准后）。
- 部署清单、环境配置、云基础设施配置。
- 将运维关注点从应用源码树中剥离。

## 规则

- 未在 `docs/05_ADR/` 留下 ADR 前，不定云厂商或编排方案。
- 密钥永不提交于此 — 本地用 `.env`，线上用密钥管理系统。
- 此处变更应引用 Architecture 文档与相关 ADR。

## 状态

Phase 0 占位。尚未定义基础设施。
