# CloudFormation EC2 Templates

このフォルダには、シンプルなEC2インスタンスを作成するためのCloudFormationテンプレートが含まれています。

## ファイル一覧

1. **simple-ec2.yaml** - フル機能版
   - 独自のVPCとサブネット作成
   - セキュリティグループ設定
   - Webサーバー（Apache）の自動インストール
   - 完全な出力情報

2. **minimal-ec2.yaml** - 最小構成版
   - デフォルトVPCを使用
   - 基本的なセキュリティグループ
   - Webサーバー（Apache）の自動インストール
   - 必要最小限の設定

## 使用方法

### 前提条件
- AWS CLIがインストールされ、設定されていること
- EC2 Key Pairが作成済みであること

### デプロイ手順

#### 1. AWS CLIを使用してデプロイ

```bash
# フル機能版をデプロイ
aws cloudformation create-stack \
  --stack-name simple-ec2-stack \
  --template-body file://simple-ec2.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=your-key-pair-name

# 最小構成版をデプロイ
aws cloudformation create-stack \
  --stack-name minimal-ec2-stack \
  --template-body file://minimal-ec2.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=your-key-pair-name
```

#### 2. AWS Management Consoleを使用してデプロイ

1. AWS Management Consoleにログイン
2. CloudFormationサービスに移動
3. 「スタックの作成」をクリック
4. 「テンプレートファイルのアップロード」を選択
5. YAMLファイルをアップロード
6. パラメータを設定（KeyNameは必須）
7. スタックを作成

### パラメータ

| パラメータ名 | 説明 | デフォルト値 | 必須 |
|-------------|------|-------------|------|
| InstanceType | EC2インスタンスタイプ | t2.micro | いいえ |
| KeyName | EC2キーペア名 | - | はい |
| SSHLocation | SSH接続を許可するCIDR範囲 | 0.0.0.0/0 | いいえ（simple-ec2.yamlのみ） |

### 出力情報

デプロイが完了すると、以下の情報が出力されます：

- **InstanceId**: EC2インスタンスのID
- **PublicIP**: パブリックIPアドレス
- **PublicDNSName**: パブリックDNS名
- **WebURL**: WebサーバーのURL
- **SSHCommand**: SSH接続コマンド

### 接続方法

#### SSH接続
```bash
ssh -i your-key-pair-name.pem ec2-user@<PublicDNSName>
```

#### Webブラウザでアクセス
```
http://<PublicDNSName>
```

### スタックの削除

```bash
aws cloudformation delete-stack --stack-name simple-ec2-stack
```

## セキュリティ注意事項

- デフォルトではSSHアクセスが全世界に開放されています（0.0.0.0/0）
- 本番環境では適切なCIDR範囲を設定してください
- 不要なポートは開放しないよう注意してください

## 料金について

- t2.microインスタンスは AWS Free Tier の対象です
- 実際の利用料金についてはAWS料金計算ツールでご確認ください

## トラブルシューティング

### よくある問題

1. **キーペアが見つからない**
   - 正しいリージョンでキーペアが作成されているか確認
   - KeyNameパラメータが正確か確認

2. **インスタンスにアクセスできない**
   - セキュリティグループの設定を確認
   - インスタンスが起動中でないか確認（数分かかる場合があります）

3. **AMIが見つからない**
   - 該当リージョンで利用可能なAMI IDに更新してください
   - 最新のAmazon Linux 2 AMIを使用することを推奨

## カスタマイズ

テンプレートは以下のようにカスタマイズできます：

- インスタンスタイプの追加
- 追加のセキュリティグループルール
- 追加のユーザーデータスクリプト
- 追加のタグ設定
- EBSボリュームの設定

## サポート

質問や問題がある場合は、AWSドキュメントのCloudFormationセクションをご参照ください。
