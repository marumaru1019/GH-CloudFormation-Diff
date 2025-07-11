# セキュリティ強化版 CloudFormation テンプレート

このドキュメントでは、`simple-ec2.yaml`に実装されたセキュリティ強化機能について説明します。

## 実装されたセキュリティ機能

### 1. ネットワークセキュリティ

#### VPC Flow Logs
- **目的**: ネットワークトラフィックの監視とログ記録
- **機能**: VPC内のすべてのネットワークトラフィックをCloudWatch Logsに記録
- **利点**: 不審なアクティビティの検出、ネットワーク分析、コンプライアンス要件の満足

#### Network ACLs (ネットワークACL)
- **目的**: サブネットレベルでのトラフィック制御
- **機能**: 
  - SSH (22): 指定されたCIDRからのみ許可
  - HTTP (80): 全世界から許可
  - HTTPS (443): 全世界から許可
  - Ephemeral Ports (1024-65535): 戻りトラフィック用
- **利点**: セキュリティグループの追加防御層

#### セキュリティグループの強化
- **送信ルール**: 明示的な送信ルールを定義
- **最小権限の原則**: 必要最小限のポートのみ開放
- **説明の追加**: 各ルールに明確な説明を追加

### 2. アクセス制御

#### SSH アクセスの制限
- **デフォルト CIDR**: `10.0.0.0/8` (プライベートネットワーク)
- **変更前**: `0.0.0.0/0` (全世界)
- **利点**: 不正なSSHアクセスの大幅な減少

#### IAM ロールとインスタンスプロファイル
- **EC2InstanceRole**: EC2インスタンス用のIAMロール
- **管理ポリシー**:
  - `CloudWatchAgentServerPolicy`: CloudWatch Agentの実行許可
  - `AmazonSSMManagedInstanceCore`: Systems Manager Session Managerの利用許可
- **利点**: キーベースのアクセスに加えて、SSM経由での安全な接続が可能

### 3. 監視とログ

#### CloudWatch Agent
- **メトリクス収集**: CPU、メモリ、ディスク使用率
- **ログ収集**: 
  - Apache アクセスログ
  - Apache エラーログ
  - システムセキュリティログ (`/var/log/secure`)
- **利点**: 詳細なシステム監視とセキュリティイベントの追跡

#### 詳細監視
- **機能**: EC2インスタンスの詳細メトリクス
- **設定**: パラメータで有効/無効を選択可能
- **利点**: より細かい粒度での監視

### 4. アプリケーションセキュリティ

#### Apache セキュリティヘッダー
- **X-Frame-Options**: DENY (クリックジャッキング攻撃を防止)
- **X-Content-Type-Options**: nosniff (MIME タイプスニッフィングを防止)
- **X-XSS-Protection**: 1; mode=block (XSS攻撃を防止)
- **Strict-Transport-Security**: HTTPS強制
- **Content-Security-Policy**: default-src 'self' (コンテンツ制限)

#### サーバー情報の隠蔽
- **ServerTokens**: Prod (サーバー情報を最小限に)
- **ServerSignature**: Off (サーバー署名を無効化)

### 5. 侵入検知と防御

#### Fail2ban
- **目的**: SSH ブルートフォース攻撃の防止
- **設定**:
  - 最大試行回数: 3回
  - バン時間: 3600秒 (1時間)
  - 監視時間: 600秒 (10分)
- **利点**: 自動的な攻撃者IPのブロック

#### 自動セキュリティ更新
- **yum-cron**: 自動セキュリティパッチ適用
- **利点**: 最新のセキュリティパッチを自動適用

### 6. 接続方法

#### SSH接続 (従来型)
```bash
ssh -i your-key-pair-name.pem ec2-user@<PublicDNSName>
```

#### SSM Session Manager (推奨)
```bash
aws ssm start-session --target <InstanceId>
```

**SSMの利点**:
- インターネット経由でのSSH不要
- セッション記録とログ
- IAMベースのアクセス制御
- キーペア不要

## セキュリティ設定の確認

### 1. VPC Flow Logsの確認
```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/vpc/flowlogs/"
```

### 2. CloudWatch Agentの状態確認
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a query-config
```

### 3. Fail2banの状態確認
```bash
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

### 4. セキュリティヘッダーの確認
```bash
curl -I http://<PublicDNSName>
```

## セキュリティのベストプラクティス

### 1. 定期的なセキュリティ監査
- CloudWatch Logsの定期的な確認
- VPC Flow Logsの分析
- 不審なアクティビティの監視

### 2. アクセス制御の最適化
- SSH CIDRの定期的な見直し
- 不要なユーザーアカウントの削除
- IAMポリシーの最小権限原則の適用

### 3. パッチ管理
- 定期的なシステム更新の確認
- 重要なセキュリティパッチの迅速な適用
- 自動更新の監視

### 4. 監視の活用
- CloudWatch アラームの設定
- 異常なメトリクスの通知
- ログの定期的な分析

## コンプライアンス

このテンプレートは以下のセキュリティ標準に準拠しています：

- **AWS Well-Architected Framework** - セキュリティの柱
- **CIS (Center for Internet Security)** - Linux セキュリティベンチマーク
- **NIST Cybersecurity Framework** - 基本的なセキュリティ統制

## 制限事項

- HTTPSの完全な実装には追加のSSL証明書設定が必要
- 本番環境では専用のログ管理ソリューションを検討することを推奨
- 高可用性が必要な場合は、マルチAZ構成を検討

## 追加推奨事項

1. **AWS Config** - リソース設定の継続的な監視
2. **AWS Security Hub** - 統合セキュリティ監視
3. **AWS GuardDuty** - 脅威検出サービス
4. **AWS Inspector** - 脆弱性評価
5. **AWS WAF** - Webアプリケーションファイアウォール（必要に応じて）
