# Migration Plan: Payment API v1 -> v2

## 1. Ly do nang cap

v2 toi uu cho mo rong quoc te va tranh ambiguity:

- `amount` (float) cua v1 de gay sai so, v2 dung `amount_cents` (int)
- `user_id` doi thanh `customer_id`
- `payment_method` string doi thanh object `method` de them metadata
- Bo sung `currency` bat buoc

## 2. Mapping schema

- `user_id` -> `customer_id`
- `amount` -> `amount_cents` (`amount * 100`)
- `payment_method` -> `method.type`
- `status` giu nguyen

## 3. Timeline deprecation

- T0: Public v2 + gui deprecation notice cho v1
- T0 + 30 ngay: Nhac lai qua changelog/email/Slack
- T0 + 60 ngay: Dong bang feature moi tren v1
- T0 + 90 ngay: Sunset v1 (tra `410 Gone` cho write endpoint neu can)

## 4. Checklist cho team consumer

- Update client call tu `/api/v1/payments` sang `/api/v2/payments`
- Doi payload theo schema v2
- Add assertion cho header `Deprecation` neu con su dung v1
- Chay regression test tren sandbox

## 5. Rollback strategy

- Duy tri route v1 read-only trong 2 tuan sau sunset
- Bat feature flag de tam mo lai write endpoint v1 khi co su co nghiem trong