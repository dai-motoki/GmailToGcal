


# GAS

### Google Apps Scriptプロジェクトの作成

1. **Google Driveにアクセス**:
   - Googleアカウントでログインし、[Google Drive](https://drive.google.com)にアクセスします。

2. **新しいApps Scriptプロジェクトの作成**:
   - 「新規」ボタンをクリックし、「その他」から「Google Apps Script」を選択します。
   - 新しいタブでApps Scriptのエディタが開きます。

3. **プロジェクトの命名**:
   - プロジェクトのタイトル部分をクリックし、プロジェクトに名前を付けます（例：「Gmail Task Manager」）。

### Gmail APIとGoogle Calendar APIの有効化

1. **Apps Scriptエディタでのサービス追加**:
   - Apps Scriptのエディタの左側にある「サービス」アイコン（プラス記号付きのマーク）をクリックします。

2. **Gmail APIの追加**:
   - 「サービスを追加」ダイアログで「Gmail API」を探し、選択します。
   - 「追加」ボタンをクリックしてGmail APIをプロジェクトに追加します。

3. **Google Calendar APIの追加**:
   - 同じく「サービスを追加」ダイアログで「Google Calendar API」を探し、選択します。
   - 「追加」ボタンをクリックしてGoogle Calendar APIをプロジェクトに追加します。

### Google Apps Scriptのコードをコピー

1. **以下のコードをコピー**:

```
function getLatestEmailBody() {
  // from:を使用して特定のアドレスからの最新のメールを検索
  var threads = GmailApp.search('from:motoki.daisuke@kandaquantum.co.jp', 0, 1);
  if (threads.length === 0) {
    throw new Error('No emails found.');
  }
  // 最新のメールを取得
  var message = threads[0].getMessages().pop();
  return message.getPlainBody(); // メールの本文を返す
}

function createCalendarEvent(task) {
  var calendar = CalendarApp.getDefaultCalendar(); // デフォルトのカレンダーを取得
  var startTime = new Date(task["期限"]); // 開始時間をDateオブジェクトに変換
  var endTime = new Date(startTime.getTime() + 15 * 60 * 1000); // 終了時間（開始時間から15分後）
  var options = {
    description: task["内容"]
  };
  calendar.createEvent('タスク: ' + task["内容"], startTime, endTime, options);
}

function processGptResponseAndCreateEvents(gptResponse) {
  // GPT-4からの応答(JSONオブジェクト)をパースしてタスクリストを取得
  var tasks = JSON.parse(gptResponse).tasks;
  
  // 各タスクについてGoogleカレンダーにイベントとして登録
  tasks.forEach(function(task) {
    createCalendarEvent(task);
  });
}

function requestGpt4Completion() {
  var emailBody = getLatestEmailBody(); // メール本文を取得

  // スクリプトプロパティからAPIキーを取得
  const apiKey = PropertiesService.getScriptProperties().getProperty('APIKEY');
  
  // GPT-4 APIのエンドポイント
  const apiUrl = 'https://api.openai.com/v1/chat/completions';
  
  // 投稿文にプロンプトとメールの本文を設定
  const prompt = `以下のメールからRFC3339タイムスタンプフォーマットYYYY-MM-DDTHH:MM:SS+09:00でタスクをリストアップしてください。期日は自分で考えて必ず記載、
  以下のような感じ。jsonのみ出力
{"tasks": [
        {
            "期限": "2023-12-01 10:00~10:15",
            "内容": "AKKODiSフリーランス運営事務局からの案件情報確認"
        },
        {
            "期限": "2023-12-01 10:15~10:30",
            "内容": "興味があれば案件の詳細をウェブサイトでチェック"
        },
        {
            "期限": "2023-12-01 10:30~10:45",
            "内容": "配信停止を検討する場合、アカウント設定からメール設定を変更"
        },]}

  `;
  const messages = [
    {'role': 'system', 'content': 'You are a helpful assistant. Please extract tasks from the following email:'},
    {'role': 'user', 'content': prompt},
    {'role': 'user', 'content': emailBody}
  ];

  // APIリクエスト用のヘッダー
  const headers = {
    'Authorization': 'Bearer ' + apiKey,
    'Content-Type': 'application/json'
  };

  // APIリクエストオプションの設定
  const options = {
    'method': 'post',
    'headers': headers,
    'muteHttpExceptions': true,
    'payload': JSON.stringify({
      'model': 'gpt-4-1106-preview',
      "response_format": { "type": "json_object" },
      'max_tokens': 2048,
      'temperature': 0.5, // より決定論的な応答を得るために温度を下げる
      'messages': messages
    })
  };

  // APIリクエスト実行
  const response = UrlFetchApp.fetch(apiUrl, options);
  const responseData = JSON.parse(response.getContentText());
  
  // レスポンスの確認
  if (responseData.error) {
    throw new Error(`GPT-4 API Error: ${responseData.error.message}`);
  }
  
  // GPT-4からの応答メッセージを取得
  const gptResponse = responseData.choices[0].message.content;
  Logger.log('GPT-4 Response:');
  Logger.log(gptResponse); // 出力結果をログに出力

  processGptResponseAndCreateEvents(gptResponse);
  


  
  // ここでタスク抽出の結果を処理する
  // 例えば、Googleカレンダーやタスク管理システムに追加するコードなど
}

function myFunction() {
  requestGpt4Completion();
}

   
```

2. **Apps Scriptエディタに貼り付け**:
   - Apps Scriptエディタのコードエディタにコードを貼り付けます。

3. **APIキーの設定**:

    1. Google Apps Scriptのエディタで、左側のメニューから「プロジェクトの設定」を選択します（歯車のアイコン）。
    2. 「スクリプトのプロパティ」タブを開きます。
    3. 新しいプロパティを追加するために「プロパティを追加」をクリックします。
    4. プロパティ名に `APIKEY`（または任意の名前）を、値にはあなたのOpenAIのAPIキーを入力します（先頭の `sk-` なども含めて）。
    5. 「保存」をクリックします。

4. **スクリプトの実行**:
   - Apps Scriptエディタのメニューから「実行」をクリックします。
   - 「アクセスを許可」ダイアログが表示されるので、「許可」をクリックします。
   - これでスクリプトが実行され、GPT-4からの応答がログに出力されます。
   - Googleカレンダーにイベントが追加されていることを確認します。


# Python での実行環境（後で書く）


   1 Google Cloud Consoleに移動します。
   2 新しいプロジェクトを作成するか、既存のものを選択します。
   3 "APIとサービス > 資格情報"セクションに移動します。
   4 "資格情報を作成"をクリックし、"OAuthクライアントID"を選択します。
   5 必要に応じて同意画面を設定します。
   6 アプリケーションタイプを"デスクトップアプリ"に設定し、名前を付けます。
   7 "作成"をクリックし���資格情報が含まれるJSONファイルをダウンロードします。
   8 ダウンロードしたファイルの名前をcredentials.jsonに変更し、現在の作業ディレクトリ(/Users/motokidaisuke/hayakawagomisan)に配置します。


# Gmail APIを有効にする

# Goolge Calendar APIを有効にする