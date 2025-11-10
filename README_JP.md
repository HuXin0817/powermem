[English](README.md) | [中文](README_CN.md) | [日本語](README_JP.md)

<p align="center">
    <a href="https://github.com/oceanbase/powermem/blob/master/LICENSE">
        <img alt="license" src="https://img.shields.io/badge/license-Apache%202.0-green.svg" />
    </a>
    <a href="https://img.shields.io/badge/python%20-3.10.0%2B-blue.svg">
        <img alt="pyversions" src="https://img.shields.io/badge/python%20-3.10.0%2B-blue.svg" />
    </a>
    <a href="https://deepwiki.com/oceanbase/powermem">
        <img alt="Ask DeepWiki" src="https://deepwiki.com/badge.svg" />
    </a>
</p>

# PowerMem - インテリジェントメモリシステム

AI アプリケーション開発において、大規模言語モデルが履歴会話、ユーザー設定、コンテキスト情報を永続的に「記憶」できるようにすることは、核心的な課題です。PowerMem は、ベクトル検索、全文検索、グラフデータベースのハイブリッドストレージアーキテクチャを組み合わせ、認知科学のエビングハウス忘却曲線理論を導入して、AI アプリケーション向けの強力なメモリインフラストラクチャを構築します。システムは、エージェントメモリの分離、エージェント間のコラボレーションと共有、きめ細かい権限制御、プライバシー保護メカニズムを含む、包括的なマルチエージェントサポート機能も提供し、複数の AI エージェントが独立したメモリ空間を維持しながら効率的なコラボレーションを実現できるようにします。

特に、PowerMem は OceanBase データベースに対して深く最適化されており、ベクトル検索と全文検索のハイブリッド検索機能、データパーティション管理のための Sub Stores サポート、自動ベクトルインデックス設定、およびさまざまなベクトルインデックスタイプ（HNSW、IVF、FLAT など）の柔軟な選択を含み、大規模なエンタープライズアプリケーションに優れたパフォーマンスとスケーラビリティを提供します。インテリジェントカスタマーサービスシステム、パーソナライズされた AI アシスタント、またはマルチエージェントコラボレーションプラットフォームを構築する場合でも、PowerMem はエンタープライズグレードのメモリ管理機能を提供し、AI が真に「記憶」能力を持つことを可能にします。

## アーキテクチャ

![アーキテクチャ図](docs/images/powermem_jp.png)

PowerMem は、以下をサポートするモジュラーアーキテクチャで構築されています：

- **コアメモリエンジン**：基本メモリ操作とインテリジェント管理
- **エージェントフレームワーク**：コラボレーションと権限を備えたマルチエージェントサポート
- **ストレージアダプター**：プラガブルなストレージバックエンド（ベクトル、グラフ、ハイブリッド）
- **グラフストレージ**：複雑なメモリ相互接続のための関係ベースのグラフストレージ
- **LLM 統合**：複数の LLM プロバイダーサポート
- **埋め込みサービス**：さまざまな埋め込みモデル統合

詳細なアーキテクチャ情報については、[アーキテクチャガイド](docs/architecture/overview.md) を参照してください。

## 主な機能

### インテリジェントメモリ管理
- **エビングハウス忘却曲線**：認知科学に基づくスマートメモリ最適化
- **自動重要度スコアリング**：AI 駆動のメモリ重要度評価
- **メモリ減衰と強化**：使用パターンに基づく動的メモリ保持
- **インテリジェント検索**：コンテキストを意識したメモリ検索とランキング

### マルチエージェントサポート
- **エージェント分離**：異なるエージェント用の独立したメモリ空間
- **エージェント間コラボレーション**：共有メモリアクセスとコラボレーショントラッキング
- **権限制御**：エージェントメモリのきめ細かいアクセス制御
- **プライバシー保護**：組み込みのプライバシー制御とデータ保護

### 複数のストレージバックエンド
- **OceanBase**：深い最適化を備えたデフォルトのエンタープライズグレードのスケーラブルなベクトルデータベース：
  - ベクトル検索と全文検索のハイブリッド検索機能
  - データパーティション管理のための Sub Stores サポート
  - 自動ベクトルインデックス設定
  - さまざまなベクトルインデックスタイプ（HNSW、IVF、FLAT など）の柔軟な選択
- **SQLite**：開発用の軽量なファイルベースのストレージ
- **PostgreSQL**：オープンソースのベクトルデータベースソリューション
- **カスタムアダプター**：拡張可能なストレージアーキテクチャ

### グラフベースのメモリストレージ
- **ナレッジグラフ**：エンティティと関係を抽出してナレッジグラフを構築
- **グラフ検索**：複雑なメモリ関係のためのマルチホップグラフトラバーサル
- **関係検索**：グラフクエリを通じてメモリ間の接続を発見
- **ハイブリッドストレージ**：ベクトル検索とグラフ関係を組み合わせて検索を強化

## クイックスタート

### インストール

```bash
# 基本インストール
pip install powermem

# LLM とベクトルストアの依存関係を含む
pip install powermem[llm,vector_stores]

# すべての依存関係を含む開発環境
pip install powermem[dev,test,llm,vector_stores,extras]
```

### 基本的な使用方法

**✨ 最も簡単な方法**：`.env` ファイルから自動的にメモリを作成！

```python
from powermem import create_memory

# .env から自動的に読み込むか、モックプロバイダーを使用
memory = create_memory()

# メモリを追加
memory.add("ユーザーはコーヒーが好き", user_id="user123")

# メモリを検索
memories = memory.search("ユーザー設定", user_id="user123")
for memory in memories:
    print(f"- {memory.get('memory')}")
```

より詳細な例と使用パターンについては、[はじめにガイド](docs/guides/0001-getting_started.md) を参照してください。

## ドキュメント

- **[はじめに](docs/guides/0001-getting_started.md)**：インストールとクイックスタートガイド
- **[設定ガイド](docs/guides/0002-configuration.md)**：完全な設定オプション
- **[マルチエージェントガイド](docs/guides/0004-multi_agent.md)**：マルチエージェントのシナリオと例
- **[統合ガイド](docs/guides/0005.integrations.md)**：LLM と埋め込みプロバイダーの統合
- **[API ドキュメント](docs/api/overview.md)**：完全な API リファレンス
- **[アーキテクチャガイド](docs/architecture/overview.md)**：システムアーキテクチャと設計
- **[例](docs/examples/overview.md)**：インタラクティブな Jupyter ノートブックとユースケース

## 開発

### 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/powermem/powermem.git
cd powermem

# 開発依存関係をインストール
pip install -e ".[dev,test,llm,vector_stores]"
```

## 貢献

貢献を歓迎します！貢献ガイドラインと行動規範をご覧ください。

## サポート

- **問題報告**：[GitHub Issues](https://github.com/oceanbase/powermem/issues)
- **ディスカッション**：[GitHub Discussions](https://github.com/oceanbase/powermem/discussions)

---

## ライセンス

このプロジェクトは Apache License 2.0 の下でライセンスされています - 詳細については [LICENSE](LICENSE) ファイルを参照してください。

