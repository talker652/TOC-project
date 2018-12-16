# F74051255 TOC Project 2019

## 介紹

### use
一開始的state是在user

有兩種輸入
	
   1. hello （開始使用）
	
   2. test (用來測試是否開始 因為有時候要等一段時間)

輸入hello之後會跳出
   ```
   Hello
	
   How can I help you?
	
   1. ....
	
   2. ....(幾個選項可以輸入）
   ```
   
   例：輸入**image**就會回傳圖片給你 ~~（然後你要在輸入please）~~ :smile::smile::smile:
   
根據輸入文字的選項不同會到達不同的state

### FSM

[image](https://raw.githubusercontent.com/talker652/TOC-project/master/fsm.png)

## 程式

### 用法
* 執行app.py
```sh
python app.py
```
* 執行ngrok
```sh
./ngrok http 5006
```

複製ngrok產生的https網址到facebook的webhook的回忽網址 後面加上/webhook

驗證權杖為1234

有連通的話分私團就能回傳訊息了（可用test測試）

### 程式function介紹
* **send_text_message（name,text）**
	
  功能：傳送文字
		
    name為收訊息的id
	
    text為要傳送的訊息
    
* **send_image_message（name,text）**
	
  功能：傳送圖片
		 
     name為收訊息的id
		 
     text為要傳送圖片的url
* **NLP_func(text）**
	
  功能：將中文具字進行斷句
		 
     text為要分斷的句子
		
     回傳分斷好的句子
	
  作法：將輸入近來的文字跟從教育部下載的字典（dict1 dict2 dict3）進行比對
  
  例：
  ```
     輸入：今天午餐吃什麼
     輸出：
          今天
          午餐
          吃
          什麼
  ```


* **Game(text)**
	
  簡單的互動遊戲

  程式隨機產生一組4位數字（0~9不重複） 讓玩家來猜

  如果猜對數字 但是位置不對 就為B

  如果位置數字都對 就為A

  例：

    答案為1234

    玩家猜1324

    結果為2A2B

* **TocMachine(GraphMachine)**
	
  設定Finite state machine在不同state下的工作

* **show_fsm()**
	
  畫出Finite state machine的圖	

**其他細節打在註解裡**

