# kh813-custom-profile-generator

## About / 概要
  
When using Google Secure LDAP + FreeRADIUS for Wi-Fi access point  
authorization (EAP-TTLS/PAP), each Mac clients needs mobileconfig  
with the authenticating username embedded.  
  
It's hard for system admins to prepare .mobileconfig for each user. 
With the app, each user can generate his/her own .mobileconfig files.  
  
Mac, iPhone, iPadなどのAppleデバイスでGoogle Secure LDAPとFreeRADIUSを   
組み合わせたバックエンドを使って無線AP接続時の認証（EAP-TTLS/PAP）を行う場合、
ユーザーアカウントが埋め込まれた.mobileconfigファイルのインストールが必要です。      
  
システム管理者がユーザーごとに.mobileconfigを生成するというのはたいへんですが、  
このアプリケーションは、選択されたテンプレートのユーザー名部分を
自分のアカウントに置き換えた.mobileconfigを自分で生成できます。    
  

## Running the app / 実行方法  

Double click the app  
実行ファイルをダブルクリック  
```
For Mac
cpg-mac.app 

For Windows 
cpg-win.exe
```

or run the script   
または、以下を実行  
```
python main.py
```


## Generating the executable file / 実行ファイルを生成  

```
With Nuitka

python build-nuitka.py

or 

with Pyinstaller

python build-pyinstaller.py
```

You'll find the executable file in dist directory  
distディレクトリに実行ファイルが生成される  

It'll generate binary depending on the running OS;   
for Windows when running on Windows,   
or for Mac when running on Mac.   
実行時のOSがWindowsならWindows向け、  
MacならMac向けの実行ファイルが生成されます  
  

### .mobileconfig

Save .mobileconfig templates in mobileconfig directory. 
The app will automatically make the list of loaded .mobileconfig files.   
  
.mobileconfigのテンプレートは、mobileconfingフォルダの中に保存してください。  
そのフォルダ内のファイルはアプリケーション起動時に自動的に一覧に追加されます。  


### パスワード埋め込み

You can embed the password within the .mobileconfig file. 
If you'd want to do that, uncomment the following liines 
```
                #data["PayloadContent"][0]["EAPClientConfiguration"]["UserPassword"] = new_password

...

## Password input field
#entry_label2 = tk.Label(input_frame, text="Your password")
#entry_label2.grid(row=1, column=0, padx=40, pady=5, sticky="w")
#
#entry_field2 = tk.Entry(input_frame, width=35, show="*")
#entry_field2.grid(row=1, column=1, padx=0, pady=5)
```

And modify the window height if needed.   
必要に応じてウィンドウの高さも調整してください

```
root.geometry("500x400")
```

## License

MIT License

